FROM debian:jessie
MAINTAINER Nadrieril "nadrieril@eleves.polytechnique.fr"

ENV HTTP_PROXY http://kuzh.polytechnique.fr:8080
ENV http_proxy http://kuzh.polytechnique.fr:8080
ENV https_proxy http://kuzh.polytechnique.fr:8080

RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

ADD nginx.conf /etc/nginx/nginx.conf

EXPOSE 8000
CMD ["nginx"]
