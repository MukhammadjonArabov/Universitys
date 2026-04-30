from django.urls import path
from university import views

app_name = 'university'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('universitetlar/', views.universities_list_view, name='universities'),
    path('universitetlar/<int:pk>/', views.university_detail_view, name='university_detail'),

    path('test/', views.test_intro_view, name='test_intro'),
    path('test/process/', views.test_process_view, name='test_process'),
    path('test/submit/', views.submit_test, name='submit_test'),
    path('test/result/<int:pk>/', views.test_result_view, name='test_result'),
    path('verify-code/', views.verify_code_view, name='verify_code'),
]