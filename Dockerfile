FROM debian:jessie
MAINTAINER Nadrieril "nadrieril@eleves.polytechnique.fr"

RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

ADD nginx.conf /etc/nginx/nginx.conf

EXPOSE 8000
CMD ["nginx"]
