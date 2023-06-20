#!/bin/sh

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

#python manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput

python -m gunicorn --bind 0.0.0.0:5000 -c gunicorn.conf.py mytable.wsgi