from __future__ import absolute_import, unicode_literals
from django_redis import get_redis_connection

from django.core.cache import cache

from celery import shared_task

@shared_task
def save_user_token_to_redis(user: str, token: str) -> None:
    """
    Description: Save the token to redis
    """
    cache.set(user, token, timeout=60 * 60 * 24 * 7)

@shared_task
def delete_user_token_from_redis(user: str) -> None:
    """
    Description: Delete the token from redis
    """
    
    cache.delete(user)

@shared_task
def is_token_valid(token: str, user: str) -> bool:
    """
    Description: Check if the token is valid
    """
    cached_token = cache.get(user)
    return cached_token == token
    