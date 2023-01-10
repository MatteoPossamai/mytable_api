from django.db import models

from accounts.models import BaseUser

class RestaurantUser(BaseUser):
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.email