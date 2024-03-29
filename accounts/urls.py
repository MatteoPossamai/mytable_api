from django.urls import path, include

from .views import RestaurantUserCreateView, RestaurantUserDeleteView, \
    RestaurantUserGetAllView, RestaurantUserGetView, RestaurantUserPutUser, \
    RestaurantUserLoginView, RestaurantUserLogoutView, RestaurantUserLogged, CreateCheckoutSessionView, \
    WebhookView, CreatePortalSessionView, GetProductsView, CustomerPortalView, GetCustomerSubscription, \
    GetRestaurantUserByRestaurant, RestaurantUserChangePassword


current_version = 'v1'

# Restaurant User
restaurant_user_urlpatterns = [
    # Read
    path('', RestaurantUserGetAllView.as_view(), name='restaurant_user_get_all'),
    path('get/<str:email>/', RestaurantUserGetView.as_view(), name='restaurant_user_get'),
    path('get-restaurant/<int:restaurant_id>/', GetRestaurantUserByRestaurant.as_view(), name='restaurant_user_get_by_restaurant'),
    # Update username or password
    path('put/', RestaurantUserPutUser.as_view(), name='restaurant_user_put'),
    path('change-password/', RestaurantUserChangePassword.as_view(), name='restaurant_user_change_password'),
    # Delete
    path('delete/', RestaurantUserDeleteView.as_view(), name='restaurant_user_delete'),
    # Signup, Login, Logout, Logged
    path('signup/', RestaurantUserCreateView.as_view(), name='restaurant_user_create'),
    path('login/', RestaurantUserLoginView.as_view(), name='restaurant_user_login'),
    path('logout/', RestaurantUserLogoutView.as_view(), name='restaurant_user_logout'),
    path('logged/', RestaurantUserLogged.as_view(), name='restaurant_user_logged'),
]

payment_urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('create-portal-session/', CreatePortalSessionView.as_view(), name='create_portal_session'),
    path('customer-portal/', CustomerPortalView.as_view(), name='customer_portal'),
    path('webhook/', WebhookView.as_view(), name='webhook'),
    path('products/', GetProductsView.as_view(), name='get_products'),
    path('costumer-subscription/', GetCustomerSubscription.as_view(), name='get_customer_subscription')
]

# ALL URLS
urlpatterns = [
    path(current_version + '/restaurant_user/', include(restaurant_user_urlpatterns)),
    path(current_version + '/stripe/', include(payment_urlpatterns)),
]