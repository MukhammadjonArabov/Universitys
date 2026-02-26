from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Prefetch
from django.core.paginator import Paginator
from django.urls import reverse

from .models import (
    University,
    Region,
    Faculty,
    Employee,
    EmployeeSubject,
    Direction,
)


def home_view(request):
    """
    Homepage with hero + Uzbekistan map showing universities with coordinates.
    """
    universities_with_geo = (
        University.objects.filter(latitude__isnull=False, longitude__isnull=False)
        .select_related("region")
        .order_by("name")
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
    faculties_count = Faculty.objects.count()
    directions_count = Direction.objects.count()

    return render(
        request,
        "home.html",
        {
            "map_data": map_data,
            "universities_geo_count": len(map_data),
            "universities_count": universities_count,
            "faculties_count": faculties_count,
            "directions_count": directions_count,
        },
    )


def universities_list_view(request):
    """
    Universities list with region filter and text search.
    """
    search_query = request.GET.get("search", "").strip()
    region_id = request.GET.get("region")

    queryset = University.objects.select_related("region").all().order_by("name")

    if region_id:
        queryset = queryset.filter(region_id=region_id)

    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(website__icontains=search_query)
            | Q(postal_address__icontains=search_query)
        )

    paginator = Paginator(queryset, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    regions = Region.objects.order_by("name")
    active_region = None
    if region_id:
        active_region = regions.filter(id=region_id).first()

    return render(
        request,
        "universities.html",
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

    faculties = (
        Faculty.objects.filter(university=university)
        .select_related("employee")
        .order_by("name")
    )

    employees = (
        university.employee.select_related("degree", "position")
        .prefetch_related(
            Prefetch(
                "employeesubject_set",
                queryset=EmployeeSubject.objects.select_related("subject"),
            )
        )
        .order_by("last_name", "first_name")
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
        "university_detail.html",
        {
            "university": university,
            "faculties": faculties,
            "employees": employees,
            "map_point": map_point,
        },
    )

def faculties_list_view(request):
    """
    Faculties list with university filter and text search.
    """
    search_query = request.GET.get("search", "").strip()
    university_id = request.GET.get("university")

    queryset = Faculty.objects.select_related("university").all().order_by("name")

    if university_id:
        queryset = queryset.filter(university_id=university_id)

    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    paginator = Paginator(queryset, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    universities = University.objects.all().order_by("name")
    active_university = None
    if university_id:
        active_university = universities.filter(id=university_id).first()

    return render(
        request,
        "faculties.html",
        {
            "universities": universities,
            "active_university": active_university,
            "page_obj": page_obj,
            "faculties": page_obj.object_list,
            "search_query": search_query,
            "selected_university_id": university_id,
        },
    )


def faculty_detail_view(request, pk):
    """
    Faculty detail page showing description, kafedras, directions, and subjects.
    """
    faculty = get_object_or_404(
        Faculty.objects.select_related("university", "employee").prefetch_related(
            "kafedras__direction_set__directionsubject_set__subject"
        ), 
        pk=pk
    )
    
    return render(
        request,
        "faculty_detail.html",
        {
            "faculty": faculty,
        },
    )
