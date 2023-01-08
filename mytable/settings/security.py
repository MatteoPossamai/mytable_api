# IMPORTING STANDARD LIBRARIES
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECURE_SSL_REDIRECT = eval(os.environ.get('SECURE_SSL_REDIRECT', 'False'))
CSRF_COOKIE_SECURE = eval(os.environ.get('CSRF_COOKIE_SECURE', 'False'))
SESSION_COOKIE_SECURE = eval(os.environ.get('SESSION_COOKIE_SECURE', 'False'))

# CSP 
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)

# HSTS
SECURE_HSTS_SECONDS = eval(os.environ.get('SECURE_HSTS_SECONDS', '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = eval(os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'False'))
SECURE_HSTS_PRELOAD = eval(os.environ.get('SECURE_HSTS_PRELOAD', 'False'))