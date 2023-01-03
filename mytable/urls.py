from django.contrib import admin
from django.urls import include, path

base_url = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(base_url, include('accounts.urls')),
    path(base_url, include('order.urls')),
    path(base_url, include('restaurant.urls')),
]
