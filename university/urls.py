from django.urls import path
from university import views

app_name = 'university'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('universitetlar/', views.universities_list_view, name='universities'),
    path('universitetlar/<int:pk>/', views.university_detail_view, name='university_detail'),
    path('manbalar/', views.resources_list_view, name='resources'),

    path('test/', views.test_intro_view, name='test_intro'),
    path('test/process/', views.test_process_view, name='test_process'),
    path('test/submit/', views.submit_test, name='submit_test'),
    path('test/result/<int:pk>/', views.test_result_view, name='test_result'),
    path('api/analyze-test/<int:pk>/', views.analyze_test_api, name='analyze_test_api'),
    path('login/', views.login_view, name='login'),
]