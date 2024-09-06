﻿"""
Django settings for geoadaptation project.

Generated by 'django-admin startproject' using Django 3.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Dotenv purpose is to hide secret key and login info from a .env file hidden on the server. Make sure you don't push
# your .env file on git and github!
from dotenv import load_dotenv
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret! Load your .env file and point the path to it to
# Django
load_dotenv()
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Here you put your IP adress
ALLOWED_HOSTS = ['139.177.197.87','.geoadaptation.ca']


# Application definition

INSTALLED_APPS = [
    "corsheaders",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django_recaptcha',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'leaflet',
    'dpd_static_support',
    # Add your app here (mine is called coresite) so Django knows where to look for your scripts
    'coresite.apps.CoresiteConfig',
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Add this line to detect user's browser language. Must be between SessionMiddleware and CommonMiddleware
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Add this line to enforce csp policy 
    # 'csp.middleware.CSPMiddleware',
    "django.middleware.common.CommonMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# To be changed, quickfixed to make leaflet and fetching tile from database with mvt_view
CORS_ALLOW_ALL_ORIGINS = True

# ALLOWED_HOSTS = [
#     "127.0.0.1",
# ]
#
# CORS_ALLOWED_ORIGINS = [
#     "http://127.0.0.1:8000",
# ]

ROOT_URLCONF = 'geoadaptation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #add csp context processors to use nonce in your template for the csp policy
                # 'csp.context_processors.nonce',
            ],
        },
    },
]


WSGI_APPLICATION = 'geoadaptation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Default database is SQLite3, here you can change the info so it points to your real database. Again, hide those
# information in your .env file before commiting to GitHub.
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': str(os.getenv('NAME')),
        'USER': str(os.getenv('USERS')),
        'PASSWORD': str(os.getenv('PASSWORD')),
        'HOST': str(os.getenv('HOST')),
        'PORT': str(os.getenv('PORT'))
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# Set folder for the translation of the site
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )

# Set the default language for your site
LANGUAGE_CODE = 'en'

# Support languages for the site. You must use a Django command in your virtual environment like :
# django-admin makemessages --ignore="static" --ignore=".env" -l fr
# to produce a folder for the language you want (here french) and make the translation in the django.po file.
# Then, you compile with :
# django-admin compilemessages
# This process can update what you already have without erasing what has already been done

LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
]

TIME_ZONE = 'UTC'

# Make sure all those value are True to effectively use I18N in your Django project
USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 2592000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_EXPIRE_AT_BROwSER_CLOSE= True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
                    )
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FROM_EMAIL = str(os.getenv('EMAIL'))
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = str(os.getenv('EMAIL_HOST'))
EMAIL_HOST_USER = str(os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_HOST_PASSWORD'))
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

RECAPTCHA_PUBLIC_KEY = str(os.getenv('RECAPTCHA_PUBLIC_KEY'))
RECAPTCHA_PRIVATE_KEY = str(os.getenv('RECAPTCHA_PRIVATE_KEY'))

# Problem with Leaflet and vectorgrid
# X_FRAME_OPTIONS = 'SAMEORIGIN'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

LEAFLET_CONFIG = {'PLUGINS': {'name-of-plugins': {
    'js': ["https://unpkg.com/leaflet.vectorgrid@latest/dist/Leaflet.VectorGrid.bundled.js"],
    'auto-include': True}}
}


# CSP_DEFAULT_SRC = ("'self'",
# # To be fixed later, problems with leaflet tag
#                    "'unsafe-inline'",)
# CSP_STYLE_SRC = ("'self'",
# # To be fixed later, problems with leaflet tag
#                 "'unsafe-inline'",
#                  'https://www.google.com/recaptcha/',
#                  'https://recaptcha.google.com/recaptcha/',
#                  'https://www.gstatic.com/recaptcha/',
#                  'https://unpkg.com',
#                  'https://cdn.jsdelivr.net',
#                  'https://fonts.googleapis.com/',
#                  'https://fonts.gstatic.com/',)
# CSP_SCRIPT_SRC = ("'self'",
# # To be fixed later, problems with leaflet tag
#                   "'unsafe-inline'",
#                   'https://www.google.com/recaptcha/',
#                   'https://recaptcha.google.com/recaptcha/',
#                   'https://www.gstatic.com/recaptcha/',
#                   'https://unpkg.com',
#                   'https://cdn.jsdelivr.net',
#                   'https://fonts.googleapis.com',
#                   'https://fonts.gstatic.com',)
# CSP_FONT_SRC = ("'self'",
#                 'https://fonts.googleapis.com',
#                 'https://fonts.gstatic.com',)
# CSP_CONNECT_SRC = ("'self'",)
# CSP_OBJECT_SRC = ("'self'", )
# CSP_BASE_URI = ("'self'", )
# CSP_FRAME_ANCESTORS = ("'self'",)
# CSP_FORM_ACTION = ("'self'",)
# CSP_INCLUDE_NONCE_IN = ("'self'","script-src","style-src")
# CSP_MANIFEST_SRC = ("'self'",)
# CSP_WORKER_SRC = ("'self'",)
# CSP_MEDIA_SRC = ("'self'",)
# CSP_FRAME_SRC = ("'self'",
#                  'https://weather.gc.ca',
#                  'https://www.google.com/recaptcha/',
#                  'https://recaptcha.google.com/recaptcha/',
#                  'https://www.gstatic.com/recaptcha/',
#                  'https://unpkg.com',
#                  'https://cdn.jsdelivr.net',
#                  'https://fonts.googleapis.com/',
#                  'https://fonts.gstatic.com/',)
# CSP_IMAGE_SRC = ("'self'",)