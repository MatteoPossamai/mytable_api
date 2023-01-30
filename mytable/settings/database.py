# IMPORTING STANDARD LIBRARIES
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# LOCAL VARIABILES
from .main import ENV_TYPE

DATABASES = {}
if ENV_TYPE == 'local' or ENV_TYPE == 'test' or ENV_TYPE == 'venv':
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
else:
    with open(os.path.join(BASE_DIR, "db_password.txt")) as f:
        PRODUCTION_DB_KEY = f.read().strip()

    DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DB_NAME', 'defaultdb'),
            'USER': os.getenv('DB_USER', 'doadmin'),
            'PASSWORD': PRODUCTION_DB_KEY,
            'HOST': os.getenv('DB_HOST', 'db-postgresql-nyc3-12345-do-user-123456-0.b.db.ondigitalocean.com'),
            'PORT': os.getenv('DB_PORT', 25060)
        }
    }
