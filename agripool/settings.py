import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'changeme-for-dev-only-not-for-production')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# CSRF Settings for Railway deployment
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://*.railway.app,https://*.up.railway.app').split(',')
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'rest_framework',
    'agri',
]

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.environ.get('MONGO_PORT', 27017))
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'agripool')
MONGODB_URL = os.environ.get('MONGODB_URL', None)

# Debug: Print what we're seeing
print("=" * 50)
print("MONGODB CONFIGURATION DEBUG")
print("=" * 50)
print(f"MONGODB_URL environment variable: {MONGODB_URL}")
print(f"MONGO_HOST: {MONGO_HOST}")
print(f"MONGO_PORT: {MONGO_PORT}")
print(f"MONGO_DBNAME: {MONGO_DBNAME}")
print("=" * 50)

# MongoDB connection via mongoengine
import mongoengine

try:
    if MONGODB_URL:
        # Use connection string (for Railway, Render, etc.)
        print(f"✓ Using MONGODB_URL connection string")
        mongoengine.connect(
            db=MONGO_DBNAME,
            host=MONGODB_URL,
            alias='default',
            serverSelectionTimeoutMS=5000
        )
    else:
        # Use individual parameters (for local development)
        print(f"✓ Using individual parameters: {MONGO_HOST}:{MONGO_PORT}/{MONGO_DBNAME}")
        mongoengine.connect(
            db=MONGO_DBNAME,
            host=MONGO_HOST,
            port=MONGO_PORT,
            alias='default',
            serverSelectionTimeoutMS=5000
        )
    print("✓ MongoDB connected successfully!")
except Exception as e:
    print(f"✗ MongoDB connection error: {e}")
    print("✗ App will start but database operations will fail until MongoDB is configured.")

# Dummy database for Django (required but not used)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'agripool.urls'
WSGI_APPLICATION = 'agripool.wsgi.application'

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
