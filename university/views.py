import json
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Prefetch
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import get_language
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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

def get_current_language(request):
    lang = getattr(request, 'LANGUAGE_CODE', None) or get_language()
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


def get_localized_field(base_name, lang):
    return f"{base_name}_{lang}"


# 20 Static Psychological Questions
STATIC_QUESTIONS = [
    {
        "id": 1,
        "text": "Sizga qaysi mashg'ulot ko'proq yoqadi?",
        "options": [
            {"id": 101, "text": "Kompyuter dasturlari bilan ishlash", "direction": "Axborot texnologiyalari"},
            {"id": 102, "text": "Odamlarni davolash va maslahat berish", "direction": "Tibbiyot"},
            {"id": 103, "text": "Chizmalar chizish va qurilmalar yaratish", "direction": "Muhandislik"},
            {"id": 104, "text": "Bolalarga dars berish", "direction": "Pedagogika"}
        ]
    },
    {
        "id": 2,
        "text": "Muammoni qanday hal qilishni afzal ko'rasiz?",
        "options": [
            {"id": 201, "text": "Mantiqiy va algoritmlar orqali", "direction": "Axborot texnologiyalari"},
            {"id": 202, "text": "Qonunlar va qoidalarga tayanib", "direction": "Huquqshunoslik"},
            {"id": 203, "text": "Raqamlar va hisob-kitoblar bilan", "direction": "Iqtisodiyot"},
            {"id": 204, "text": "Ijodiy yondashib", "direction": "San'at"}
        ]
    },
    {
        "id": 3,
        "text": "Kelajakda o'zingizni kim sifatida ko'rasiz?",
        "options": [
            {"id": 301, "text": "Katta kompaniya rahbari", "direction": "Iqtisodiyot"},
            {"id": 302, "text": "Mashhur advokat yoki sudya", "direction": "Huquqshunoslik"},
            {"id": 303, "text": "Malakali shifokor", "direction": "Tibbiyot"},
            {"id": 304, "text": "Dasturchi yoki muhandis", "direction": "Axborot texnologiyalari"}
        ]
    },
    {
        "id": 4,
        "text": "Siz uchun eng qiziqarli fan qaysi edi?",
        "options": [
            {"id": 401, "text": "Matematika va fizika", "direction": "Muhandislik"},
            {"id": 402, "text": "Biologiya va kimyo", "direction": "Tibbiyot"},
            {"id": 403, "text": "Tarix va adabiyot", "direction": "Gumanitar fanlar"},
            {"id": 404, "text": "Informatika", "direction": "Axborot texnologiyalari"}
        ]
    },
    {
        "id": 5,
        "text": "Yangi narsalarni qanday o'rganishni yoqtirasiz?",
        "options": [
            {"id": 501, "text": "Tajribada sinab ko'rib", "direction": "Muhandislik"},
            {"id": 502, "text": "Boshqalarga tushuntirib berib", "direction": "Pedagogika"},
            {"id": 503, "text": "Mustaqil o'qib va tahlil qilib", "direction": "Gumanitar fanlar"},
            {"id": 504, "text": "Kompyuterda o'rganib", "direction": "Axborot texnologiyalari"}
        ]
    },
    {
        "id": 6,
        "text": "Ish joyingiz qanday bo'lishini xohlaysiz?",
        "options": [
            {"id": 601, "text": "Zamonaviy ofisda kompyuter qarshisida", "direction": "Axborot texnologiyalari"},
            {"id": 602, "text": "Kasalxonada yoki laboratoriyada", "direction": "Tibbiyot"},
            {"id": 603, "text": "Qurilish maydonida yoki zavodda", "direction": "Muhandislik"},
            {"id": 604, "text": "Maktabda yoki universitetda", "direction": "Pedagogika"}
        ]
    },
    {
        "id": 7,
        "text": "Sizda qaysi xususiyat kuchliroq?",
        "options": [
            {"id": 701, "text": "Diqqatlilik va aniqlik", "direction": "Iqtisodiyot"},
            {"id": 702, "text": "Sabr-toqat va mehribonlik", "direction": "Tibbiyot"},
            {"id": 703, "text": "Adolatparvarlik", "direction": "Huquqshunoslik"},
            {"id": 704, "text": "Kreativlik", "direction": "San'at"}
        ]
    },
    {
        "id": 8,
        "text": "Qaysi xorijiy tilni o'rganish sizga qiziq?",
        "options": [
            {"id": 801, "text": "Ingliz tili (biznes uchun)", "direction": "Iqtisodiyot"},
            {"id": 802, "text": "Lotin tili (tibbiyot uchun)", "direction": "Tibbiyot"},
            {"id": 803, "text": "Dasturlash tillari", "direction": "Axborot texnologiyalari"},
            {"id": 804, "text": "Badiiy tarjima uchun tillar", "direction": "Gumanitar fanlar"}
        ]
    },
    {
        "id": 9,
        "text": "Kutilmagan vaziyatda nima qilasiz?",
        "options": [
            {"id": 901, "text": "Yechimni tezda hisoblayman", "direction": "Iqtisodiyot"},
            {"id": 902, "text": "Vaziyatni qonuniy baholayman", "direction": "Huquqshunoslik"},
            {"id": 903, "text": "Tezkor yordam ko'rsataman", "direction": "Tibbiyot"},
            {"id": 904, "text": "Texnik nosozlikni tuzataman", "direction": "Muhandislik"}
        ]
    },
    {
        "id": 10,
        "text": "Sizga nima ko'proq zavq beradi?",
        "options": [
            {"id": 1001, "text": "Yangi ilova yoki sayt yaratish", "direction": "Axborot texnologiyalari"},
            {"id": 1002, "text": "Bemorning sog'ayishi", "direction": "Tibbiyot"},
            {"id": 1003, "text": "Siyosiy debatlarda qatnashish", "direction": "Huquqshunoslik"},
            {"id": 1004, "text": "Yangi loyihani moliyalashtirish", "direction": "Iqtisodiyot"}
        ]
    },
    {
        "id": 11,
        "text": "Siz qanday kitoblarni yoqtirasiz?",
        "options": [
            {"id": 1101, "text": "Ilmiy-texnik adabiyotlar", "direction": "Muhandislik"},
            {"id": 1102, "text": "Detektiv va huquqiy asarlar", "direction": "Huquqshunoslik"},
            {"id": 1103, "text": "Sog'lom turmush tarzi haqida", "direction": "Tibbiyot"},
            {"id": 1104, "text": "Biznes va psixologiya", "direction": "Iqtisodiyot"}
        ]
    },
    {
        "id": 12,
        "text": "Guruhda qanday rol o'ynaysiz?",
        "options": [
            {"id": 1201, "text": "Boshqaruvchi (Lider)", "direction": "Iqtisodiyot"},
            {"id": 1202, "text": "G'oyalar generatori", "direction": "San'at"},
            {"id": 1203, "text": "Ijrochi (Texnik mutaxassis)", "direction": "Axborot texnologiyalari"},
            {"id": 1204, "text": "Maslahatchi va tarbiyachi", "direction": "Pedagogika"}
        ]
    },
    {
        "id": 13,
        "text": "Sizni nima ko'proq tashvishlantiradi?",
        "options": [
            {"id": 1301, "text": "Iqtisodiy inqirozlar", "direction": "Iqtisodiyot"},
            {"id": 1302, "text": "Ekologik muammolar va kasalliklar", "direction": "Tibbiyot"},
            {"id": 1303, "text": "Inson huquqlari buzilishi", "direction": "Huquqshunoslik"},
            {"id": 1304, "text": "Texnologik orqada qolish", "direction": "Axborot texnologiyalari"}
        ]
    },
    {
        "id": 14,
        "text": "Siz qanday o'yinlarni yoqtirasiz?",
        "options": [
            {"id": 1401, "text": "Strategik va mantiqiy", "direction": "Iqtisodiyot"},
            {"id": 1402, "text": "Simulyatorlar (shifokor, uchuvchi)", "direction": "Tibbiyot"},
            {"id": 1403, "text": "Action va sarguzasht", "direction": "Muhandislik"},
            {"id": 1404, "text": "Kibersport o'yinlari", "direction": "Axborot texnologiyalari"}
        ]
    },
    {
        "id": 15,
        "text": "Odamlar bilan qanday muloqot qilasiz?",
        "options": [
            {"id": 1501, "text": "Rasmiy va aniq faktlar asosida", "direction": "Huquqshunoslik"},
            {"id": 1502, "text": "Ishontirish orqali (notiq)", "direction": "Pedagogika"},
            {"id": 1503, "text": "Yaqin va samimiy", "direction": "Tibbiyot"},
            {"id": 1504, "text": "Ijtimoiy tarmoqlar orqali", "direction": "Axborot texnologiyalari"}
        ]
    },
    {
        "id": 16,
        "text": "Siz uchun muvaffaqiyat nima?",
        "options": [
            {"id": 1601, "text": "Yuqori daromadli biznes", "direction": "Iqtisodiyot"},
            {"id": 1602, "text": "Insonlar hayotini saqlab qolish", "direction": "Tibbiyot"},
            {"id": 1603, "text": "Global ahamiyatga ega texnologiya", "direction": "Axborot texnologiyalari"},
            {"id": 1604, "text": "Qadriyatlarni saqlab qolish", "direction": "Gumanitar fanlar"}
        ]
    },
    {
        "id": 17,
        "text": "Qaysi sohada kashfiyot qilmoqchisiz?",
        "options": [
            {"id": 1701, "text": "Sun'iy intellekt", "direction": "Axborot texnologiyalari"},
            {"id": 1702, "text": "Gen muhandisligi", "direction": "Tibbiyot"},
            {"id": 1703, "text": "Kosmik kemalar", "direction": "Muhandislik"},
            {"id": 1704, "text": "Yangi iqtisodiy model", "direction": "Iqtisodiyot"}
        ]
    },
    {
        "id": 18,
        "text": "Sizga nima ko'proq yoqadi?",
        "options": [
            {"id": 1801, "text": "Binolar dizayni", "direction": "Muhandislik"},
            {"id": 1802, "text": "Grafik dizayn", "direction": "San'at"},
            {"id": 1803, "text": "Matnlar bilan ishlash", "direction": "Gumanitar fanlar"},
            {"id": 1804, "text": "Ma'lumotlar bazasi", "direction": "Axborot texnologiyalari"}
        ]
    },
    {
        "id": 19,
        "text": "Dunyoni nima qutqaradi deb o'ylaysiz?",
        "options": [
            {"id": 1901, "text": "Ilm-fan va texnologiya", "direction": "Axborot texnologiyalari"},
            {"id": 1902, "text": "Mehribonlik va tibbiyot", "direction": "Tibbiyot"},
            {"id": 1903, "text": "Adolat va qonun ustuvorligi", "direction": "Huquqshunoslik"},
            {"id": 1904, "text": "Iqtisodiy farovonlik", "direction": "Iqtisodiyot"}
        ]
    },
    {
        "id": 20,
        "text": "Keyingi 10 yil ichida qaysi soha eng muhim bo'ladi?",
        "options": [
            {"id": 2001, "text": "Raqamlashtirish (IT)", "direction": "Axborot texnologiyalari"},
            {"id": 2002, "text": "Virusologiya va sog'liqni saqlash", "direction": "Tibbiyot"},
            {"id": 2003, "text": "Ekologik energiya", "direction": "Muhandislik"},
            {"id": 2004, "text": "Ta'lim islohotlari", "direction": "Pedagogika"}
        ]
    }
]


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
                "name": uni.name,
                "region": uni.region.name if uni.region else "",
                "phone_number": uni.phone_number,
                "email": uni.email,
                "lat": uni.latitude,
                "lng": uni.longitude,
                "detail_url": reverse("university:university_detail", args=[uni.id]),
            }
        )

    # Get counts from database
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




def test_intro_view(request):
    """Intro page for the psychological test."""
    return render(request, "pages/test_intro.html")


@login_required(login_url="/verify-code/")
def test_process_view(request):
    """The psychological test process page with 20 static questions and timer."""
    # Use static questions instead of DB
    return render(request, "pages/test_process.html", {"questions": STATIC_QUESTIONS})


@login_required
def submit_test(request):
    """Handle test submission via AJAX or POST."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            answers = data.get("answers", {}) # {question_id: option_id}
            
            # Calculate scores per direction name
            direction_scores = {}
            for q_id_str, opt_id_str in answers.items():
                q_id = int(q_id_str)
                opt_id = int(opt_id_str)
                
                # Find option in static list
                found = False
                for q in STATIC_QUESTIONS:
                    if q["id"] == q_id:
                        for opt in q["options"]:
                            if opt["id"] == opt_id:
                                d_name = opt["direction"]
                                direction_scores[d_name] = direction_scores.get(d_name, 0) + 1
                                found = True
                                break
                    if found: break
            
            # Always set default recommendation as it will be updated by Gemini later.
            recommendation = "Gemini AI natijalaringizni tahlil qilmoqda..."

            # Save result
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
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    return redirect("university:test_intro")


from django.views.decorators.http import require_POST
import environ
from google import genai

env = environ.Env()

@login_required
def test_result_view(request, pk):
    """Display test result."""
    result = get_object_or_404(UserTestResult, pk=pk, user=request.user)
    return render(request, "pages/test_result.html", {"result": result})

@login_required
@require_POST
def analyze_test_api(request, pk):
    result = get_object_or_404(UserTestResult, pk=pk, user=request.user)
    
    lang = get_current_language(request)
    lang_map = {'uz': 'Uzbek', 'ru': 'Russian', 'en': 'English'}
    target_lang = lang_map.get(lang, 'Uzbek')
    
    scores_text = "\\n".join([f"- {k}: {v} points" for k, v in result.score_data.items()])
    
    prompt = f"""
You are an expert career counselor and psychologist. 
A student has completed a psychological career test and got the following scores in different fields:
{scores_text}

Analyze these results and provide a highly motivating, personalized, and professional career recommendation.
Explain briefly why these fields fit the student based on their scores. Do not format as a letter, just return the raw text. Use markdown for bolding.
IMPORTANT: You MUST write your entire response in {target_lang} language!
"""
    try:
        client = genai.Client(api_key=env('GEMINI_API_KEY'))
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        recommendation_text = response.text
        
        result.recommendation = recommendation_text
        result.save()
        
        return JsonResponse({"status": "success", "recommendation": recommendation_text})
    except Exception as e:
        print("Gemini API Error:", e)
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def login_view(request):
    """Render the beautifully designed Google login page."""
    if request.user.is_authenticated:
        return redirect("university:test_process")
    return render(request, "auth/login.html")
