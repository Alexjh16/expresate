import os
from pathlib import Path
from ..settings import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'tu-secret-key')

ALLOWED_HOSTS = [
    'expresate-backend-2024.fly.dev',
    'localhost',
    '127.0.0.1'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    "django_htmx",
    'users',
    'contenidos',
    'seguimiento',
    'evaluacion',
    'expresate',
    'mongoData',
    'modelos_expresate',
    'modulo_evaluacionEstudiante',
    'django_seed',
    'django_altcha',
    'corsheaders',
    'tailwind',
    'theme',
    'django_browser_reload',
    'django_alpine',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

ROOT_URLCONF = 'expresate.urls'

WSGI_APPLICATION = 'expresate.wsgi.application'

# Database - Usar DATABASE_URL de Fly.io
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# MongoDB
MONGODB_URI = os.environ.get('MONGODB_URI')

# Redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL'),
    }
}

REDIS = {
    "HOST": os.environ.get('REDIS_HOST', 'localhost'),
    "PORT": int(os.environ.get('REDIS_PORT', 6379)),
    "DB": int(os.environ.get('REDIS_DB', 0)),
    "PASSWORD": os.environ.get('REDIS_PASSWORD', None),
}

# Altcha configuration
ALTCHA_SECRET_KEY = os.environ.get('ALTCHA_SECRET_KEY', 'key_1k07u2ceuNfftdDGhw7w6')
ALTCHA_ALGORITHM = 'SHA-256'

# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'contenidos.middleware.AuthRequiredMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]

# CORS
CORS_ALLOWED_ORIGINS = [
    "https://expresate-backend-2024.fly.dev",
    "http://localhost:3000",
]