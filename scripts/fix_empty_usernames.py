"""Fix users with empty username created earlier by social logins.

Run from project root inside the virtualenv:

    .venv\Scripts\python.exe scripts\fix_empty_usernames.py

This script sets a generated unique username for any User with an empty
username field.
"""
import os
import sys

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

import re


def _generate_unique_username(base_value: str) -> str:
    base = (base_value or 'user')
    base = re.sub(r'[^A-Za-z0-9._-]', '', base)
    if not base:
        base = 'user'
    candidate = base
    suffix = 0
    while User.objects.filter(username=candidate).exists():
        suffix += 1
        candidate = f"{base}{suffix}"
    return candidate


updated = 0
for u in User.objects.filter(username=""):
    new_username = _generate_unique_username(u.email or str(u.pk))
    u.username = new_username
    u.save()
    print(f"Updated user id={u.pk} -> username={new_username}")
    updated += 1

print(f"Done. Updated {updated} users.")
