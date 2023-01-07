# IMPORTING STANDARD LIBRARIES
import os

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'restaurant': os.environ.get("RESTAURANT_API_RATE_LIMIT"),
        'category': os.environ.get("CATEGORY_API_RATE_LIMIT"),
        'item': os.environ.get("ITEM_API_RATE_LIMIT"),
        'order': os.environ.get("ORDER_API_RATE_LIMIT"),
        'takes': os.environ.get("TAKES_API_RATE_LIMIT"),
        'user': os.environ.get("USER_API_RATE_LIMIT"),
    },
    #'PAGE_SIZE': eval(os.getenv("PAGE_SIZE")),
    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}