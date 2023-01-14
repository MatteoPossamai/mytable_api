# IMPORTING STANDARD PACKAGES
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER", "redis://6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_BROKER", "redis://6379/0")

# REDIS
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# TTL SETTINGS
CACHE_TTL_USER = os.getenv("CACHE_TTL_USER", 60 * 60 * 24 * 7)  # 7 days
CACHE_TTL_OBJECT = os.getenv("CACHE_TTL_OBJECT", 60 * 60 * 3)  # 3 hours
NEW_OBJECT_TTL = os.getenv("NEW_OBJECT_TTL", 60 * 60 * 1)  # 1 hour

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