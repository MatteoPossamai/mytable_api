from django.urls import path, include

from .views import OrderCreateView, OrderGetAllView, OrderGetView, OrderPutView, \
    OrderDeleteView, TakesGetAllView, TakesGetAllByOrder, TakesGetSingleView

current_version = 'v1'

# Order
order_urlpatterns = [
    # Create
    path('create/', OrderCreateView.as_view(), name='order_create'),
    # Read
    path('', OrderGetAllView.as_view(), name='order_get_all'),
    path('get/<int:pk>/', OrderGetView.as_view(), name='order_get'),
    # Update
    path('put/<int:pk>/', OrderPutView.as_view(), name='order_put'),
    # Delete
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
]

take_urlpatterns = [
    # Create
    # Read
    path('', TakesGetAllView.as_view(), name='takes_get_all'),
    path('get/<int:order_pk>/', TakesGetAllByOrder.as_view(), name='takes_get_all_by_order'),
    path('get/<int:pk>/', TakesGetSingleView.as_view(), name='takes_get_single'),
    # Update
    # Delete
]

# ALL URLS
urlpatterns = [
    path(current_version + '/order/', include(order_urlpatterns)),
    path(current_version + '/take/', include(take_urlpatterns)),
]
