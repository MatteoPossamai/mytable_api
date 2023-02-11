# IMPORTING STANDARD LIBRARIES
import os

# IMPORTING THIRD PARTY PACKAGES
from corsheaders.defaults import default_headers

# DJANGO CORS CONFIGURATIONS
if os.getenv('CORS_ALLOWED_ORIGINS') is not None:
    CORS_ALLOWED_ORIGINS = eval(os.getenv('CORS_ALLOWED_ORIGINS'))
elif os.getenv('CORS_ALLOWED_ORIGIN_REGEXES') is not None:
    CORS_ALLOWED_ORIGIN_REGEXES = eval(os.getenv('CORS_ALLOWED_ORIGIN_REGEXES'))
elif os.getenv("CORS_ALLOW_ALL_ORIGINS") is not None:
    CORS_ALLOW_ALL_ORIGINS = True

#CORS_ALLOW_HEADERS = list(default_headers) + eval(os.getenv('CORS_ALLOW_HEADERS'))
CORS_ALLOW_METHODS = eval(os.getenv('CORS_ALLOW_METHODS'))

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "Access-Control-Allow-Origin",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Methods",
    "HTTP_TOKEN",
    "http_token",
    "HTTP_AUTHORIZATION",
    "HTTP_ORIGIN",
    "TOKEN",
    "token"
]

CORS_ORIGIN_ALLOW_ALL = True