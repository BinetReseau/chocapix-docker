FROM debian:jessie

RUN apt-get update && \
    apt-get install -y gunicorn python-flask python-requests

RUN mkdir /app
WORKDIR /app
ADD . /app

VOLUME /srv/off
CMD gunicorn app:app -b unix:/srv/off/gunicorn.sock --log-level=error --log-file=-
