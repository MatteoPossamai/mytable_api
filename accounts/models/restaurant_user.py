from django.db import models

from accounts.models import BaseUser

class RestaurantUser(BaseUser):
    level = models.IntegerField(default=0)
    stripe_customer_id = models.CharField(max_length=100)
    has_used_free_trial = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.email