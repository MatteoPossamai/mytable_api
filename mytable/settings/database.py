# IMPORTING STANDARD LIBRARIES
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# LOCAL VARIABILES
from .admin import DEBUG

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {}
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME', "my_table_postgres"),
        'USER': os.environ.get('DB_USER', "postgres"),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', 5432)
    }
}