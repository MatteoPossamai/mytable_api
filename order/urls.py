from django.urls import path, include

from .views import OrderCreateView, OrderGetAllView, OrderGetView, OrderPutView, \
    OrderDeleteView, TakesGetAllView, TakesGetAllByOrder, TakesGetSingleView, \
        TakesUpdateView, TakesDeleteView, TakesDeleteAllByOrder, TakesDeleteAllByRestaurant, \
        TakesCreateView, OrderUpdateStatusView, OrderUpdatePaymentStatusView, OrderDeleteAll

current_version = 'v1'

# Order
order_urlpatterns = [
    # Create
    path('create/', OrderCreateView.as_view(), name='order_create'),
    # Read
    path('', OrderGetAllView.as_view(), name='order_get_all'),
    path('<int:pk>/', OrderGetView.as_view(), name='order_get'),
    # Update
    path('put/<int:pk>/', OrderPutView.as_view(), name='order_put'),
    path('update/status/<int:pk>/', OrderUpdateStatusView.as_view(), name='order_update_status'),
    path('update/payment_status/<int:pk>/', OrderUpdatePaymentStatusView.as_view(), name='order_update_payment_status'),
    # Delete
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('delete/', OrderDeleteAll.as_view(), name='order_delete_all'),
]

take_urlpatterns = [
    # Create
    path('create/', TakesCreateView.as_view(), name='takes_create'),
    # Read
    path('', TakesGetAllView.as_view(), name='takes_get_all'),
    path('get/<int:pk>/', TakesGetSingleView.as_view(), name='takes_get_single'),
    path('get/order/<int:order_pk>/', TakesGetAllByOrder.as_view(), name='takes_get_all_by_order'),
    # Update
    path('put/<int:pk>/', TakesUpdateView.as_view(), name='takes_put'),
    # Delete
    path('delete/<int:pk>/', TakesDeleteView.as_view(), name='takes_delete'),
    path('delete/order/<int:order_pk>/', TakesDeleteAllByOrder.as_view(), name='takes_delete_all_by_order'),
    path('delete/restaurant/<int:restaurant_pk>/', TakesDeleteAllByRestaurant.as_view(), name='takes_delete_all_by_restaurant'),
]

# ALL URLS
urlpatterns = [
    path(current_version + '/order/', include(order_urlpatterns)),
    path(current_version + '/take/', include(take_urlpatterns)),
]
