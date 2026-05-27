"""
Setup script: Creates/updates Django Site and Google SocialApp in the database.
Run from project root: python scripts/setup_oauth.py
"""
import os
import sys
import django

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import environ
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

client_id = env('GOOGLE_CLIENT_ID', default='')
secret = env('GOOGLE_CLIENT_SECRET', default='')
site_domain = env('SITE_DOMAIN', default='localhost:8000')
site_name = env('SITE_NAME', default='Universitys Local')

# Update the Site entry (id=1 is Django's default)
site, _ = Site.objects.update_or_create(
    id=1,
    defaults={'domain': site_domain, 'name': site_name}
)
print(f"[OK] Site: id={site.id}, domain={site.domain}")

# Create or update the Google SocialApp
app, created = SocialApp.objects.update_or_create(
    provider='google',
    defaults={
        'name': 'Google OAuth',
        'client_id': client_id,
        'secret': secret,
    }
)
# Attach to site if not already linked
app.sites.add(site)
status = "created" if created else "updated"
print(f"[OK] SocialApp {status}: provider=google, client_id={client_id[:15]}...")
print("Done! Google OAuth is now configured in the database.")
