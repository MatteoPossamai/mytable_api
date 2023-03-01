from multiprocessing import cpu_count
from os import environ

# Server Socket
bind = '0.0.0.0:' + environ.get('PORT', '443')
max_requests = 1000
workers = cpu_count()
timeout = 30

# Logging
loglevel ='info'
accessformat = '%(t)s %(h)s %(l)s %(r)s %(s)s %(b)s %(f)s %(a)s'
accesslog = '-'
errorlog = '-'

# SSL
certfile = '/etc/letsencrypt/live/domain.it/fullchain.pem'
keyfile = '/etc/letsencrypt/live/domain.it/privkey.pem'
ssl_version = 2