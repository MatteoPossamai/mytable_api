from __future__ import absolute_import, unicode_literals
from django_redis import get_redis_connection

from celery import shared_task

@shared_task
def save_user_token_to_redis(user: int, token: str):
    
    redis = get_redis_connection()
    redis.set(f'user:{user}:token', token, ex=60 * 60 * 24 * 7)