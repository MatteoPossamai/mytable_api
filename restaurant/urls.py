from django.urls import path, include

from .views import RestaurantCreateView, RestaurantGetAllView, RestaurantGetView, \
    RestaurantPutView, RestaurantDeleteView, ItemCreateView, ItemGetAllView, ItemGetView, \
    ItemPutView, ItemDeleteView, CategoryCreateView, CategoryGetAllView, CategoryGetView, \
    CategoryPutView, CategoryDeleteView, CategoryGetAllActiveView, \
    ItemsChangeNumberView, CategoriesChangeNumberView, ItemsChangeActiveView,  \
    CategoriesChangeActiveView, RestaurantChangePlan, CategoryGetAllRestaurant, CategoriesBulkUpdate, \
    ItemGetByRestaurantView, ItemGetByRestaurantActiveView, ItemGetByCategoryView, ItemGetByCategoryActiveView, \
    ItemsBulkUpdate    

current_version = 'v1'

# Category
category_urlpatterns = [
    # Create
    path('create/', CategoryCreateView.as_view(), name='category_create'),
    # Read
    path('', CategoryGetAllView.as_view(), name='category_get_all'),
    path('restaurant_category/<int:pk>/', CategoryGetAllRestaurant.as_view(), name='category_get_all_restaurant'),
    path('restaurant_category/active/<int:pk>/', CategoryGetAllActiveView.as_view(), name='category_get_all_active'),
    path('<int:pk>/', CategoryGetView.as_view(), name='category_get'),
    # Update
    path('put/<int:pk>/', CategoryPutView.as_view(), name='category_put'),
    path('change-number/', CategoriesChangeNumberView.as_view(), name='category_change_number'),
    path('change-active/', CategoriesChangeActiveView.as_view(), name='category_change_active'),
    path('bulk_update/', CategoriesBulkUpdate.as_view(), name='category_bulk_update'),
    # Delete
    path('delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
]

# Item
item_urlpatterns = [
    # Create
    path('create/', ItemCreateView.as_view(), name='item-create'),
    # Read
    path('', ItemGetAllView.as_view(), name='item-get-all'),
    path('<int:pk>/', ItemGetView.as_view(), name='item-get'),
    path('restaurant_item/<int:pk>/', ItemGetByRestaurantView.as_view(), name='item-get-by-restaurant'),
    path('restaurant_item/active/<int:pk>/', ItemGetByRestaurantActiveView.as_view(), name='item-get-by-restaurant-active'),
    path('category_item/<int:pk>/', ItemGetByCategoryView.as_view(), name='item-get-by-category'),
    path('category_item/active/<int:pk>/', ItemGetByCategoryActiveView.as_view(), name='item-get-by-category-active'),    
    # Update
    path('put/<int:pk>/', ItemPutView.as_view(), name='item-put'),
    path('change-number/', ItemsChangeNumberView.as_view(), name='item-change-number'),
    path('change-active/', ItemsChangeActiveView.as_view(), name='item-change-active'),
    path('bulk_update/', ItemsBulkUpdate.as_view(), name='item_bulk_update'),
    # Delete
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='item-delete'),
]

# Restaurant
restaurant_urlpatterns = [
    # Create
    path('create/', RestaurantCreateView.as_view(), name='restaurant-create'),
    # Read
    path('', RestaurantGetAllView.as_view(), name='restaurant-get-all'),
    path('<int:pk>/', RestaurantGetView.as_view(), name='restaurant-detail'),
    # Update
    path('put/<int:pk>/', RestaurantPutView.as_view(), name='restaurant-put'),
    path('change-plan/<int:pk>/', RestaurantChangePlan.as_view(), name='restaurant-change-plan'),
    # Delete
    path('delete/<int:pk>/', RestaurantDeleteView.as_view(), name='restaurant-delete'),
]

# ALL URLS
urlpatterns = [
    path(current_version + '/category/', include(category_urlpatterns)),
    path(current_version +'/item/', include(item_urlpatterns)),
    path(current_version +'/restaurant/', include(restaurant_urlpatterns)),
]