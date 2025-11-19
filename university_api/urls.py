from django.urls import include, path

from university_api.views import UniversityDetailView, UniversityListView

urlpatterns = [
    path('university/<int:pk>/', UniversityDetailView.as_view(), name='university_detail'),
    path('universitys/', UniversityListView.as_view(), name='universitys_list'),
]