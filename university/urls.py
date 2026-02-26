from django.urls import path
from university import views

app_name = 'university'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('universitetlar/', views.universities_list_view, name='universities'),
    path('universitetlar/<int:pk>/', views.university_detail_view, name='university_detail'),
    path('fakultetlar/', views.faculties_list_view, name='faculties'),
    path('fakultetlar/<int:pk>/', views.faculty_detail_view, name='faculty_detail'),
]