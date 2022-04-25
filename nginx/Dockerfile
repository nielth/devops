FROM nginx:1.21.6-alpine
RUN rm /etc/nginx/conf.d/default.conf && \
    apk update && \
    apk add --update certbot-nginx && \
    mkdir /etc/letsencrypt && \
COPY ./conf.d/nginx.conf /etc/nginx/conf.d
COPY ./letsencrypt/archive/nielth.com/ /etc/nginx
EXPOSE 1337