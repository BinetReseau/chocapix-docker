FROM debian:jessie

ENV HTTP_PROXY http://kuzh.polytechnique.fr:8080
ENV http_proxy http://kuzh.polytechnique.fr:8080
ENV https_proxy http://kuzh.polytechnique.fr:8080

RUN apt-get update && \
    apt-get install -y gunicorn python-flask python-requests

RUN mkdir /app
WORKDIR /app
ADD . /app

VOLUME /srv/ooshop
CMD gunicorn app:app -b unix:/srv/ooshop/gunicorn.sock --log-level=error --log-file=-
