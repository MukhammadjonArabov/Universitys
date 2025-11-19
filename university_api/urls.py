from django.urls import include, path

from university_api.views import UniversityDetailView

urlpatterns = [
    path('university/<int:pk>/', UniversityDetailView.as_view(), name='university_detail'),
]