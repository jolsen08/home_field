"""
Django settings for homefield project.
HomeField - A platform for homeschoolers to join sports leagues
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-e&1yi@==^tj(_cv62r=r&s!!n4m^(j5(5xut0tbh(!-26dv^%i')

# Environment: 'test' or 'production'
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'test')

DEBUG = ENVIRONMENT == 'test'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'leagues',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'homefield.urls'

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

WSGI_APPLICATION = 'homefield.wsgi.application'


# =============================================================================
# DATABASE CONFIGURATION (AWS RDS PostgreSQL)
# =============================================================================

# Test Database - Set these environment variables:
#   DB_TEST_NAME, DB_TEST_USER, DB_TEST_PASSWORD, DB_TEST_HOST, DB_TEST_PORT

# Production Database (not yet configured) - Set these environment variables:
#   DB_PROD_NAME, DB_PROD_USER, DB_PROD_PASSWORD, DB_PROD_HOST, DB_PROD_PORT

if ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_PROD_NAME', 'homefield'),
            'USER': os.environ.get('DB_PROD_USER'),
            'PASSWORD': os.environ.get('DB_PROD_PASSWORD'),
            'HOST': os.environ.get('DB_PROD_HOST'),
            'PORT': os.environ.get('DB_PROD_PORT', '5432'),
            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }
else:
    # Test Database (default)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_TEST_NAME', 'homefield_test'),
            'USER': os.environ.get('DB_TEST_USER'),
            'PASSWORD': os.environ.get('DB_TEST_PASSWORD'),
            'HOST': os.environ.get('DB_TEST_HOST'),
            'PORT': os.environ.get('DB_TEST_PORT', '5432'),
        }
    }

# =============================================================================


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'accounts.User'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'leagues:dashboard'
LOGOUT_REDIRECT_URL = 'home'
