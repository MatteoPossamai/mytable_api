from django.urls import path, include

from .views import RestaurantUserCreateView, \
    RestaurantUserGetAllView, RestaurantUserGetView, RestaurantUserPutView, \
    RestaurantUserDeleteView, RestaurantUserLoginView


current_version = 'v1'

# Restaurant User
restaurant_user_urlpatterns = [
    # Create
    path('create/', RestaurantUserCreateView.as_view(), name='restaurant_user_create'),
    # Read
    path('', RestaurantUserGetAllView.as_view(), name='restaurant_user_get_all'),
    path('get/<int:pk>/', RestaurantUserGetView.as_view(), name='restaurant_user_get'),
    # Update
    path('put/<int:pk>/', RestaurantUserPutView.as_view(), name='restaurant_user_put'),
    # Delete
    path('delete/<int:pk>/', RestaurantUserDeleteView.as_view(), name='restaurant_user_delete'),
    # Login, Logout
    path('login/', RestaurantUserLoginView.as_view(), name='restaurant_user_login'),
]

# ALL URLS
urlpatterns = [
    path(current_version + '/restaurant_user/', include(restaurant_user_urlpatterns)),
]