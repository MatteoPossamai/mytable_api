#!/bin/bash
# the script expects two arguments:
# - the domain name for which we are obtaining the ssl certificatee
# - the Email address associated with the ssl certificate
echo DOMAIN= "api.my-table.it" > .env
echo EMAIL= "mpossamaim@gmail.com" >> .env

# Phase 1 "Initiation"
docker-compose -f ./docker-compose-first.yaml up -d nginx
docker-compose -f ./docker-compose-first.yaml up certbot
docker-compose -f ./docker-compose-first.yaml down

# Phase 2 "Operation"    
crontab ./etc/crontab
docker-compose -f ./docker-compose.yaml up -d