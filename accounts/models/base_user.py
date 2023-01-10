from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseUser(AbstractUser):
    """
    Base user class
    """
    language = models.CharField(max_length=2, default='it')

    def __str__(self):
        return self.email