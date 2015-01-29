FROM nodesource/node:wheezy
MAINTAINER Nadrieril "nadrieril@eleves.polytechnique.fr"

ENV HTTP_PROXY http://kuzh.polytechnique.fr:8080
ENV http_proxy http://kuzh.polytechnique.fr:8080
ENV https_proxy http://kuzh.polytechnique.fr:8080

RUN apt-get update && apt-get install -y python-pip supervisor nginx gunicorn python-dev libmysqlclient-dev
RUN pip install supervisor-stdout
RUN npm install -g npm && \
    npm install -g bower gulp grunt


WORKDIR /srv/app/client
ADD client/package.json /srv/app/client/
ADD client/.bowerrc /srv/app/client/
ADD client/bower.json /srv/app/client/
RUN npm install && \
    bower install --allow-root

WORKDIR /srv/app/server
ADD server/requirements.txt /srv/app/server/
RUN pip install -r requirements.txt


ADD client /srv/app/client
WORKDIR /srv/app/client
RUN sed -i 's/\(APIURL.url\).\+$/\1 = "api";/' app/app.js && \
    gulp build

ADD server /srv/app/server
WORKDIR /srv/app/server
RUN sed -i 's/bars_django\.settings\.dev_local/bars_django.settings.prod/' bars_django/wsgi.py && \
    sed -i 's/bars_django\.settings\.dev_local/bars_django.settings.prod/' manage.py && \
    echo yes | python manage.py collectstatic


ADD supervisord.conf /etc/supervisord.conf
ADD nginx.conf /etc/nginx/nginx.conf
WORKDIR /srv/app

EXPOSE 8000
CMD cd /srv/app/server && python manage.py migrate && \
    supervisord -c /etc/supervisord.conf -n
