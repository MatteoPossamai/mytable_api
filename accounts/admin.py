from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models 
from accounts.models import BaseUser
from accounts.models import RestaurantUser

admin.site.register(BaseUser)
admin.site.register(RestaurantUser)
