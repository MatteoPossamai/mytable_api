import os
from .admin import BASE_DIR

# AUTHENTICATION
STRIPE_SECRET = ''
with open(os.path.join(BASE_DIR, "stripe_secret.txt")) as f:
    STRIPE_SECRET = f.read().strip()
    