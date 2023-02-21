# APPLICATION DEFINITION
BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
]

THIRD_PARTY_APPS = [
    "django_grpc_framework",
    "corsheaders",
    "rest_framework",
    "channels",
]

LOCAL_APPS = [
    'accounts',
    'order',
    'restaurant',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_PARTY_APPS