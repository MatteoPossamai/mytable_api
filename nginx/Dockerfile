FROM nginx:1.19.0-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN mkdir -p /usr/src/app
COPY init-letsencrypt.sh /usr/src/app
WORKDIR /usr/src/app
RUN chmod +x init-letsencrypt.sh
ENTRYPOINT ["/usr/src/app/init-letsencrypt.sh"]