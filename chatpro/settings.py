"""
Django settings for chatpro project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
import environ

env = environ.Env()
env.read_env(os.path.join('.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v2+a(f76b33#t-jy(6a8=kf2p#2my=nhf(@%ezi$(j_yn_(%*s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [env("CSRF_TRUSTED_ORIGINS")]

# CORS_ORIGIN_WHITELIST = (
#     'http://localhost:3000',
#     'http://localhost:8000',
# )

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chatapp',
    'frontendapp',
    'messageapp',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'storages'
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

ROOT_URLCONF = 'chatpro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# WSGI_APPLICATION = 'chatpro.wsgi.application'
ASGI_APPLICATION = "chatpro.asgi.application"


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ]
}

LOGIN_URL = '/login/'
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': env("NAME"),

        'USER': env("DB_USER"),

        'PASSWORD': env("PASSWORD"),

        'HOST': env("HOST"),

        'PORT': env("PORT"),

    }

}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts": [(os.getenv('REDIS_HOST', 'redis'), int(os.getenv('REDIS_PORT', 6379)))],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST', 'redis')}:{os.getenv('REDIS_PORT', 6379)}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY") 
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME") 
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
AWS_S3_FILE_OVERWRITE = env.bool("AWS_S3_FILE_OVERWRITE")

if not DEBUG:
    STORAGES = {

        # Media file (image) management   
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        },
        
        # CSS and JS file management
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        },
    }

