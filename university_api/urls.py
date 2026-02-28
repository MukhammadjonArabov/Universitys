from django.urls import path
from university_api.views import UniversityDetailView, UniversityListView
from university_api.views_bot import BotSyncUserView

urlpatterns = [
    path('university/<int:pk>/', UniversityDetailView.as_view(), name='university_detail'),
    path('universitys/', UniversityListView.as_view(), name='universitys_list'),
    path('bot/sync-user/', BotSyncUserView.as_view(), name='bot-sync-user'),
]