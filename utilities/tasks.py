from __future__ import absolute_import, unicode_literals
from django_redis import get_redis_connection

from django.core.cache import cache
from celery import shared_task
import jwt

from mytable.settings import CACHE_TTL_USER, CACHE_TTL_OBJECT, JWT_SECRET

@shared_task
def save_user_token_to_redis(token: str) -> None:
    """
    Description: Save the token to redis
    """
    cache.set(token, True, timeout=int(CACHE_TTL_USER))

@shared_task
def delete_token_from_redis(token: str) -> None:
    """
    Description: Delete the token from redis
    """
    cache.delete(token)

@shared_task
def is_token_valid(token: str) -> bool:
    """
    Description: Check if the token is valid
    """
    return cache.get(token)

@shared_task
def is_token_owner(token: str, owner: str) -> bool:
    """
    Description: Check if the token is owned by the owner user
    """
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return decoded['user'] == owner
    except Exception as e:
        return False
    