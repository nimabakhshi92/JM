"""
Django settings for kalamenoor project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ygqb4!4^qrtrhyxjj%gvb)m$@9%=hi28bo&t3ops&+)uy6g&rg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['*' ,'141.11.42.252', '141.11.42.252:81', '127.0.0.1', 'localhost']
ALLOWED_HOSTS = ['5.61.24.114', '127.0.0.1', 'aynolhayat.com', 'www.aynolhayat.com', '5.61.24.114:4000',
                 '185.243.48.16']


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'ahadis.apps.AhadisConfig',
    'corsheaders'

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'

]
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'kalamenoor.urls'

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

WSGI_APPLICATION = 'kalamenoor.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'JM',
        'USER': 'root',
        'PASSWORD': 'newpassword',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
# STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'kalamenoor', 'static'))
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

from datetime import timedelta

SIMPLE_JWT = {
    # "ACCESS_TOKEN_LIFETIME": timedelta(seconds=0),
    # "REFRESH_TOKEN_LIFETIME": timedelta(seconds=0),
    # "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    # "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1000),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2000),
    "ROTATE_REFRESH_TOKENS": True,
    "TOKEN_OBTAIN_SERIALIZER": "ahadis.serializers.MyTokenObtainPairSerializer",
}
