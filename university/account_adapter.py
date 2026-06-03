from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
import re


User = get_user_model()


def _generate_unique_username(base_value: str) -> str:
    """Generate a simple unique username based on base_value.

    Strips unsafe chars, falls back to 'user' and appends a numeric suffix
    until the username is unique in the User model.
    """
    if not base_value:
        base_value = 'user'
    # keep only safe chars
    base = re.sub(r'[^A-Za-z0-9._-]', '', base_value)
    if not base:
        base = 'user'

    candidate = base
    suffix = 0
    while User.objects.filter(username=candidate).exists():
        suffix += 1
        candidate = f"{base}{suffix}"
    return candidate


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """Ensure a unique, non-empty username is set for social signups.

    Some deployments use the default `User` model which requires a unique
    `username`. Google social logins sometimes leave `username` empty which
    causes IntegrityError. This adapter populates `username` from the
    email local-part or generates a unique username.
    """

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        # Try to set username from email local-part
        email = data.get('email') or sociallogin.account.extra_data.get('email')
        if email:
            local = email.split('@')[0]
            user.username = local
        return user

    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        if not user.username:
            # Fallback: generate a unique username from email local-part or account uid
            email = getattr(user, 'email', None) or sociallogin.account.extra_data.get('email')
            base = (email.split('@')[0] if email and '@' in email else sociallogin.account.uid)
            user.username = _generate_unique_username(base)
        return super().save_user(request, sociallogin, form)
