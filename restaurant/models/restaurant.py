from django.db import models

from accounts.models import RestaurantUser

class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=False)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    description = models.TextField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(RestaurantUser, on_delete=models.CASCADE, related_name='restaurants')

    def __str__(self):
        return self.name