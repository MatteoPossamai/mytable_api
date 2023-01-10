from django.db import models

from accounts.models import RestaurantUser

class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    plan = models.JSONField()
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    description = models.TextField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=100, default=None, null=True)
    licence_expiration = models.DateTimeField(default=None, null=True)

    owner = models.ForeignKey(RestaurantUser, on_delete=models.CASCADE, related_name='restaurants')