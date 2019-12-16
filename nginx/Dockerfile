FROM nginx:1.17.4-alpine

RUN apk update \
    && apk add openssl

COPY ./generate_certs.sh /temp/
RUN chmod +x /temp/generate_certs.sh

RUN rm /etc/nginx/conf.d/default.conf
COPY ./default.conf /etc/nginx/conf.d
COPY ./dist /usr/share/nginx/html

RUN /bin/sh /temp/generate_certs.sh
