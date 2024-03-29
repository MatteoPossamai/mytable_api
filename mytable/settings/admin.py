# IMPORTING STANDARD PACKAGES
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(os.path.join(BASE_DIR, "secret_key.txt")) as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = eval(os.getenv("DEBUG"))
ALLOWED_HOSTS = eval(os.getenv("ALLOWED_HOSTS"))

MIDDLEWARE = [
    # For CSRF in future 
    # https://docs.djangoproject.com/en/4.1/ref/csrf/#ajax
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# STANDARD URL
ROOT_URLCONF = f'{os.getenv("ROOT_DIR")}.urls'
WSGI_APPLICATION = f'{os.getenv("ROOT_DIR")}.wsgi.application'

# Internationalization
TIME_ZONE = os.getenv("TIME_ZONE")
USE_TZ = eval(os.getenv("USE_TZ"))

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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

AUTH_USER_MODEL = 'accounts.BaseUser'
