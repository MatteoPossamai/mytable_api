import os
from .admin import BASE_DIR

# AUTHENTICATION
STRIPE_SECRET = ''
with open(os.path.join(BASE_DIR, "stripe_secret.txt")) as f:
    STRIPE_SECRET = f.read().strip()
    
# PRODCUTS
BASIC_MENU = os.getenv("BASIC_MENU", default=None)
IMAGE_MENU = os.getenv("IMAGE_MENU", default=None)
CLIENT_ORDER = os.getenv("CLIENT_ORDER", default=None)
WAITER_ORDER = os.getenv("WAITER_ORDER", default=None)
