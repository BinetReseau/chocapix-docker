FROM nodesource/node:wheezy
MAINTAINER Nadrieril "nadrieril@eleves.polytechnique.fr"

ENV HTTP_PROXY http://kuzh.polytechnique.fr:8080
ENV http_proxy http://kuzh.polytechnique.fr:8080
ENV https_proxy http://kuzh.polytechnique.fr:8080

RUN apt-get update && apt-get install -y python-pip supervisor nginx gunicorn
# RUN pip install gunicorn
RUN pip install supervisor-stdout
RUN npm install -g npm
RUN npm install -g bower gulp grunt

WORKDIR /srv/app/client
ADD client/package.json /srv/app/client/package.json
RUN npm install
ADD client/.bowerrc /srv/app/client/.bowerrc
ADD client/bower.json /srv/app/client/bower.json
RUN bower install --allow-root

ADD server/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD supervisord.conf /etc/supervisord.conf
ADD nginx.conf /etc/nginx/nginx.conf
ADD . /srv/app/
RUN sed -i 's/\(APIURL.url\).\+/\1 = "api";/' app/app.js
RUN gulp build

WORKDIR /srv/app/server
sed -i 's/bars_django\.settings\.dev_local/bars_django.settings.dev_server/' bars_django/wsgi.py
sed -i 's/bars_django\.settings\.dev_local/bars_django.settings.dev_server/' manage.py
RUN echo yes | python manage.py collectstatic

WORKDIR /srv/app
RUN service nginx stop

EXPOSE 8000
CMD supervisord -c /etc/supervisord.conf -n
