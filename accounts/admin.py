from django.contrib import admin

# Models 
from accounts.models import BaseUser
from accounts.models import RestaurantUser

admin.site.register(BaseUser)
admin.site.register(RestaurantUser)
