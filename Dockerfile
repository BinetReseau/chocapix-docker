FROM nodesource/node:wheezy
MAINTAINER Nadrieril "nadrieril@eleves.polytechnique.fr"

RUN apt-get -qq update && apt-get install -y python-pip supervisor nginx gunicorn
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

RUN service nginx stop

WORKDIR /srv/app
ADD . /srv/app/

EXPOSE 8000
CMD supervisord -c /etc/supervisord.conf -n
