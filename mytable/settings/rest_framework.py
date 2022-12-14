# IMPORTING STANDARD LIBRARIES
import os

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'restaurant': os.getenv("RESTAURANT_API_RATE_LIMIT"),
        'category': os.getenv("CATEGORY_API_RATE_LIMIT"),
        'item': os.getenv("ITEM_API_RATE_LIMIT"),
        'order': os.getenv("ORDER_API_RATE_LIMIT"),
        'takes': os.getenv("TAKES_API_RATE_LIMIT"),
        'user': os.getenv("USER_API_RATE_LIMIT"),
    },
    #'PAGE_SIZE': eval(os.getenv("PAGE_SIZE")),
    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}