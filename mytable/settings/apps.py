# APPLICATION DEFINITION
BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    "django_grpc_framework",
    "corsheaders",
    "rest_framework"
]

LOCAL_APPS = [
    'accounts',
    'order',
    'restaurant',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_PARTY_APPS