# IMPORTING STANDARD LIBRARIES
import os

# IMPORTING THIRD PARTY PACKAGES
from corsheaders.defaults import default_headers

# DJANGO CORS CONFIGURATIONS
if os.environ.get('CORS_ALLOWED_ORIGINS') is not None:
    CORS_ALLOWED_ORIGINS = eval(os.environ.get('CORS_ALLOWED_ORIGINS'))
elif os.environ.get('CORS_ALLOWED_ORIGIN_REGEXES') is not None:
    CORS_ALLOWED_ORIGIN_REGEXES = eval(os.environ.get('CORS_ALLOWED_ORIGIN_REGEXES'))
elif os.environ.get("CORS_ALLOW_ALL_ORIGINS") is not None:
    CORS_ALLOW_ALL_ORIGINS = eval(os.environ.get("CORS_ALLOW_ALL_ORIGINS"))

CORS_ALLOW_HEADERS = list(default_headers) + eval(os.environ.get('CORS_ALLOW_HEADERS'))
CORS_ALLOW_METHODS = eval(os.environ.get('CORS_ALLOW_METHODS'))