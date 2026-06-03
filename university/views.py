import json
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings

from .models import (
    University,
    Region,
    Direction,
    Profile,
    TestQuestion,
    TestOption,
    UserTestResult,
    AdditionalResource,
)
from .utils import get_current_language, get_localized_field, get_translation
from .services import GeminiAIService, TestAnalysisService
from .test_questions import get_test_questions

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# PUBLIC VIEWS
# ─────────────────────────────────────────────

def home_view(request):
    """
    Homepage with hero + Uzbekistan map showing universities with coordinates.
    """
    lang = get_current_language(request)
    name_field = get_localized_field("name", lang)

    universities_with_geo = (
        University.objects.filter(latitude__isnull=False, longitude__isnull=False)
        .select_related("region")
        .order_by(name_field)
    )

    map_data = []
    for uni in universities_with_geo:
        map_data.append(
            {
                # Use the language-aware field directly instead of .name property
                "name": getattr(uni, name_field, uni.name_uz),
                "region": getattr(uni.region, f"name_{lang}", uni.region.name_uz) if uni.region else "",
                "phone_number": uni.phone_number,
                "email": uni.email,
                "lat": uni.latitude,
                "lng": uni.longitude,
                "detail_url": reverse("university:university_detail", args=[uni.id]),
            }
        )

    universities_count = University.objects.count()

    return render(
        request,
        "pages/home.html",
        {
            "map_data": map_data,
            "universities_geo_count": len(map_data),
            "universities_count": universities_count,
        },
    )


def universities_list_view(request):
    """
    Universities list with region filter and text search.
    """
    lang = get_current_language(request)
    name_field = get_localized_field("name", lang)
    address_field = get_localized_field("postal_address", lang)
    region_name_field = get_localized_field("name", lang)

    search_query = request.GET.get("search", "").strip()
    region_id = request.GET.get("region")

    queryset = University.objects.select_related("region").all().order_by(name_field)

    if region_id and region_id.isdigit():
        queryset = queryset.filter(region_id=int(region_id))

    if search_query:
        queryset = queryset.filter(
            Q(**{f"{name_field}__icontains": search_query})
            | Q(email__icontains=search_query)
            | Q(website__icontains=search_query)
            | Q(**{f"{address_field}__icontains": search_query})
        )

    paginator = Paginator(queryset, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    regions = Region.objects.order_by(region_name_field)
    active_region = None
    if region_id and region_id.isdigit():
        active_region = regions.filter(id=int(region_id)).first()

    return render(
        request,
        "pages/universities.html",
        {
            "regions": regions,
            "active_region": active_region,
            "page_obj": page_obj,
            "universities": page_obj.object_list,
            "search_query": search_query,
            "selected_region_id": region_id,
        },
    )


def university_detail_view(request, pk):
    """
    Detail page with faculties, employees, and subjects.
    """
    university = get_object_or_404(
        University.objects.select_related("region"), pk=pk
    )

    map_point = None
    if university.latitude and university.longitude:
        map_point = {
            "name": university.name,
            "lat": university.latitude,
            "lng": university.longitude,
        }

    return render(
        request,
        "pages/university_detail.html",
        {
            "university": university,
            "map_point": map_point,
        },
    )


def resources_list_view(request):
    """
    List of additional resources/links.
    """
    lang = get_current_language(request)
    title_field = get_localized_field("title", lang)
    resources = AdditionalResource.objects.order_by(title_field)
    return render(request, "pages/resources.html", {"resources": resources})


# ─────────────────────────────────────────────
# AUTH VIEWS
# ─────────────────────────────────────────────

def login_view(request):
    """Render the beautifully designed Google login page."""
    if request.user.is_authenticated:
        # Redirect to home page, not test — let user decide where to go
        return redirect("university:home")
    return render(request, "auth/login.html")


@login_required
def profile_view(request):
    """User profile page showing basic profile and their test results."""
    profile = getattr(request.user, 'profile', None)
    test_results = request.user.test_results.order_by('-created_date') if request.user.is_authenticated else []
    return render(request, 'auth/profile.html', {
        'profile': profile,
        'test_results': test_results,
    })


# ─────────────────────────────────────────────
# TEST VIEWS
# ─────────────────────────────────────────────

def test_intro_view(request):
    """Intro page for the psychological test."""
    last_result = None
    if request.user.is_authenticated:
        last_result = (
            UserTestResult.objects
            .filter(user=request.user, is_completed=True)
            .order_by('-created_date')
            .first()
        )
    return render(request, "pages/test_intro.html", {"last_result": last_result})


@login_required
def test_process_view(request):
    """The psychological test process page with 20 questions and timer."""
    lang = get_current_language(request)
    questions = get_test_questions(lang)
    return render(request, "pages/test_process.html", {"questions": questions})


@login_required
@require_POST
def submit_test(request):
    """Handle test submission via AJAX POST."""
    try:
        data = json.loads(request.body)
        answers = data.get("answers", {})  # {question_id: option_id}

        # Calculate scores using language-agnostic (uz) question list
        questions = get_test_questions('uz')
        direction_scores = {}

        for q_id_str, opt_id_str in answers.items():
            try:
                q_id = int(q_id_str)
                opt_id = int(opt_id_str)
            except (ValueError, TypeError):
                continue

            for q in questions:
                if q["id"] == q_id:
                    for opt in q["options"]:
                        if opt["id"] == opt_id:
                            d_name = opt.get("direction", "Unknown")
                            direction_scores[d_name] = direction_scores.get(d_name, 0) + 1
                            break
                    break

        if not direction_scores:
            return JsonResponse(
                {"status": "error", "message": get_translation("no_valid_answers", get_current_language(request))},
                status=400
            )

        lang = get_current_language(request)
        recommendation = get_translation("analyzing", lang)

        result = UserTestResult.objects.create(
            user=request.user,
            score_data=direction_scores,
            recommendation=recommendation,
            is_completed=True
        )

        return JsonResponse({
            "status": "success",
            "redirect_url": reverse("university:test_result", args=[result.id])
        })

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": get_translation("invalid_json", get_current_language(request))}, status=400)
    except Exception as e:
        logger.error(f"submit_test error: {e}", exc_info=True)
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@login_required
def test_result_view(request, pk):
    """Display test result — only the owner can view."""
    result = get_object_or_404(UserTestResult, pk=pk, user=request.user)
    return render(request, "pages/test_result.html", {"result": result})


@login_required
@require_POST
def analyze_test_api(request, pk):
    """
    Call Gemini AI to analyze test results.
    Cached: if a rich recommendation already exists, returns it immediately.
    """
    result = get_object_or_404(UserTestResult, pk=pk, user=request.user)
    lang = get_current_language(request)
    cache_prefix = f"<!-- lang:{lang} -->"

    # Cache is language-aware; changing the site language must produce matching AI text.
    if result.recommendation and result.recommendation.startswith(cache_prefix) and len(result.recommendation) > 150:
        logger.info(f"[analyze_test_api] Returning cached result for pk={pk}, lang={lang}")
        recommendation = result.recommendation.replace(cache_prefix, "", 1).strip()
        return JsonResponse({"status": "success", "recommendation": recommendation})

    if not result.score_data:
        return JsonResponse({"status": "error", "message": get_translation("api_error", lang)}, status=400)

    ai_service = GeminiAIService()
    success, recommendation_text = ai_service.analyze_test_results(
        score_data=result.score_data,
        language=lang,
    )

    if success:
        result.recommendation = f"{cache_prefix}\n{recommendation_text}"
        result.save(update_fields=["recommendation", "updated_date"])
        return JsonResponse({"status": "success", "recommendation": recommendation_text})

    user_message = get_translation("api_error", lang)
    return JsonResponse({"status": "error", "message": user_message}, status=500)
