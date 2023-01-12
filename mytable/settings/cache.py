# IMPORTING STANDARD PACKAGES
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER", "redis://6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_BROKER", "redis://6379/0")

# REDIS
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": os.getenv("REDIS_KEY_PREFIX", "mytable")
    }
}