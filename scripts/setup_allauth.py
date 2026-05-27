import os

# 1. Update .env
env_path = '.env'
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        content = f.read()
    if 'GOOGLE_CLIENT_ID' not in content:
        with open(env_path, 'a') as f:
            f.write('\n# Google OAuth Settings\n')
            f.write('GOOGLE_CLIENT_ID=your_google_client_id\n')
            f.write('GOOGLE_CLIENT_SECRET=your_google_client_secret\n')
        print("Updated .env")

# 2. Update config/settings.py
settings_path = 'config/settings.py'
with open(settings_path, 'r', encoding='utf-8') as f:
    settings_content = f.read()

# Add allauth apps
if 'allauth' not in settings_content:
    old_apps = "    'django_filters',\n\n    #app"
    new_apps = "    'django_filters',\n\n    # Allauth\n    'django.contrib.sites',\n    'allauth',\n    'allauth.account',\n    'allauth.socialaccount',\n    'allauth.socialaccount.providers.google',\n\n    #app"
    settings_content = settings_content.replace(old_apps, new_apps)

# Add allauth middleware
if 'allauth.account.middleware.AccountMiddleware' not in settings_content:
    old_mid = "    'django.middleware.clickjacking.XFrameOptionsMiddleware',\n]"
    new_mid = "    'django.middleware.clickjacking.XFrameOptionsMiddleware',\n    'allauth.account.middleware.AccountMiddleware',\n]"
    settings_content = settings_content.replace(old_mid, new_mid)

# Add allauth configs
if 'AUTHENTICATION_BACKENDS' not in settings_content:
    configs = """
# Allauth Configuration
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

LOGIN_REDIRECT_URL = '/test/process/'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_LOGIN_ON_GET = True

# We will pull these from .env, but handle defaults
GOOGLE_CLIENT_ID = env('GOOGLE_CLIENT_ID', default='')
GOOGLE_CLIENT_SECRET = env('GOOGLE_CLIENT_SECRET', default='')

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_CLIENT_SECRET,
            'key': ''
        }
    }
}
"""
    settings_content += configs

with open(settings_path, 'w', encoding='utf-8') as f:
    f.write(settings_content)
print("Updated settings.py")
