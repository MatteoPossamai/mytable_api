from django.urls import path, include

from .views import RestaurantUserCreateView, \
    RestaurantUserGetAllView, RestaurantUserGetView, RestaurantUserPutUserName, \
    RestaurantUserDeleteView, RestaurantUserLoginView, RestaurantUserLogoutView, RestaurantUserLogged, \
    RestaurantUserPutPassword


current_version = 'v1'

# Restaurant User
restaurant_user_urlpatterns = [
    # Read
    path('', RestaurantUserGetAllView.as_view(), name='restaurant_user_get_all'),
    path('get/<str:email>/', RestaurantUserGetView.as_view(), name='restaurant_user_get'),
    # Update username
    path('put/<str:email>/', RestaurantUserPutUserName.as_view(), name='restaurant_user_put'),
    # Update password
    path('put/password/<str:email>/', RestaurantUserPutPassword.as_view(), name='restaurant_user_put_password'),
    # Delete
    path('delete/<str:email>/', RestaurantUserDeleteView.as_view(), name='restaurant_user_delete'),
    # Signup, Login, Logout, Logged
    path('signup/', RestaurantUserCreateView.as_view(), name='restaurant_user_create'),
    path('login/', RestaurantUserLoginView.as_view(), name='restaurant_user_login'),
    path('logout/', RestaurantUserLogoutView.as_view(), name='restaurant_user_logout'),
    path('logged/', RestaurantUserLogged.as_view(), name='restaurant_user_logged'),
]

# ALL URLS
urlpatterns = [
    path(current_version + '/restaurant_user/', include(restaurant_user_urlpatterns)),
]