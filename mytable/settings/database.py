# IMPORTING STANDARD LIBRARIES
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# LOCAL VARIABILES
from .admin import DEBUG

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {}
if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', "my_table_postgres"),
        'USER': os.getenv('DB_USER', "postgres"),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', 5432)
    }
}

print(f"DATABASES: {DATABASES}")