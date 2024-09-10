"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from decouple import config
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django_celery_beat",
    "django_celery_results",
    "django_filters",
    "rest_framework",
    "drf_standardized_errors",

    "api",
    "core",
    "database",
    "middleware",
    "tasks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        'BACKEND': "django.template.backends.django.DjangoTemplates",
        'DIRS': [
            BASE_DIR / "templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Django REST Framework
# https://www.django-rest-framework.org/tutorial/quickstart/

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ["helpers.response.ResponseRenderer"],
    'EXCEPTION_HANDLER': "drf_standardized_errors.handler.exception_handler",
    'DEFAULT_VERSIONING_CLASS': "core.api_versioning.APIVersioning",
    'DEFAULT_VERSION': "v1",
}


# DRF Standardized Errors
# https://drf-standardized-errors.readthedocs.io/en/latest/settings.html

DRF_STANDARDIZED_ERRORS = {
    'EXCEPTION_FORMATTER_CLASS': "helpers.exception.StandardExceptionFormatter",
}


# Celery
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url

CELERY_TIMEZONE = config('DJANGO_TIMEZONE', default="Asia/Jakarta", cast=str)

CELERY_BROKER_URL = config('REDIS_URL', default="redis://localhost:6379/0")

CELERY_CACHE_BACKEND = "django-cache"

CELERY_RESULT_BACKEND = "django-db"

CELERY_RESULT_EXTENDED = True


# Cache
# https://docs.djangoproject.com/en/5.1/topics/cache/

CACHES = {
    'default': {
        'BACKEND': "django_redis.cache.RedisCache",
        'LOCATION': config('REDIS_URL', default="redis://localhost:6379/0"),
        'TIMEOUT': 300,
        'OPTIONS': {
            'CLIENT_CLASS': "django_redis.client.DefaultClient",
            'PARSER_CLASS': "redis.connection._HiredisParser",
            'COMPRESSOR': "django_redis.compressors.lz4.Lz4Compressor",
        },
    }
}


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql",
        'NAME': config('DB_NAME', default="postgres", cast=str),
        'USER': config('DB_USER', default="postgres", cast=str),
        'PASSWORD': config('DB_PASS', default="postgres", cast=str),
        'HOST': config('DB_HOST', default="localhost", cast=str),
        'PORT': config('DB_PORT', default=5432, cast=int),
    }
}


# Session
# https://docs.djangoproject.com/en/5.1/topics/http/sessions/

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

SESSION_CACHE_ALIAS = "default"


# Authentication and authorization
# https://docs.djangoproject.com/en/5.1/topics/auth/customizing/

AUTHENTICATION_BACKENDS = [
    "core.authentication.AuthenticationBackend",
]

JWT_ALGORITHM = "HS256"

JWT_EXP_HOURS = 24


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {'NAME': "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {'NAME': "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {'NAME': "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.ScryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = config('DJANGO_LANGCODE', default="en-us", cast=str)

TIME_ZONE = config('DJANGO_TIMEZONE', default="Asia/Jakarta", cast=str)

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / "static"
    ]
else:
    STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "uploads"


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Logging
# https://docs.djangoproject.com/en/5.1/topics/logging/

FILE_HANDLER = "logging.FileHandler"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "{levelname} {asctime} {module} {message}",
            'style': "{",
        },
        'simple': {
            'format': "{message}",
            'style': "{",
        },
    },
    'handlers': {
        'console': {
            'level': "INFO",
            'class': "rich.logging.RichHandler",
            'formatter': "simple",
        },
        'file': {
            'level': "WARNING",
            'class': FILE_HANDLER,
            'filename': BASE_DIR / "logs" / "django.log",
            'formatter': "verbose",
        },
        'celery_beat': {
            'level': "INFO",
            'class': FILE_HANDLER,
            'filename': BASE_DIR / "logs" / "celery_beat.log",
            'formatter': "verbose",
        },
        'celery_worker': {
            'level': "INFO",
            'class': FILE_HANDLER,
            'filename': BASE_DIR / "logs" / "celery_worker.log",
            'formatter': "verbose",
        },
    },
    'root': {
        'handlers': ["console"],
        'level': "DEBUG",
    },
    'loggers': {
        'django': {
            'handlers': ["file"],
            'level': "INFO",
            'propagate': True,
        },
        'celery': {
            'handlers': ["celery_worker"],
            'level': "INFO",
            'propagate': True,
        },
        'django_celery_beat': {
            'handlers': ["celery_beat"],
            'level': "INFO",
            'propagate': True,
        }
    },
}


# Sentry
# https://docs.sentry.io/platforms/python/configuration/options/

SENTRY_DSN = config('SENTRY_DSN', default=None, cast=str)

if not DEBUG and SENTRY_DSN:
    from sentry_sdk import init
    init(dsn=f"{SENTRY_DSN}", traces_sample_rate=1.0, profiles_sample_rate=1.0)
