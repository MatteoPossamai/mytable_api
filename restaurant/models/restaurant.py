from django.db import models
from django.contrib.postgres.fields import ArrayField

from accounts.models import RestaurantUser

class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=False)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    description = models.TextField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    color_palette = ArrayField(ArrayField(models.CharField(max_length=30)), max_length=10, default=list(["#530F26", "#FFB01D", "#ffffff", "#E5E5E5", "#32324D"]))
    border = models.IntegerField(default=10)

    owner = models.ForeignKey(RestaurantUser, on_delete=models.CASCADE, related_name='restaurants')

    def __str__(self):
        return self.name