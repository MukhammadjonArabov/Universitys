from django.urls import path
from university.views import index

app_name = 'university'

urlpatterns = [
    path('', index, name='index'),
]