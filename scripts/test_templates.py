import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.template.loader import render_to_string
from django.test import RequestFactory
from django.urls import reverse

rf = RequestFactory()
request = rf.get('/')
request.LANGUAGE_CODE = 'uz'

templates_to_test = [
    'layouts/base.html',
    'pages/home.html',
    'pages/universities.html',
    'pages/university_detail.html',
    'pages/resources.html',
    'pages/test_intro.html',
    'pages/test_process.html',
    'pages/test_result.html',
    'auth/login_telegram.html'
]

for t in templates_to_test:
    try:
        render_to_string(t, request=request)
        print(f"Successfully rendered {t}")
    except Exception as e:
        print(f"Error rendering {t}: {e}")
