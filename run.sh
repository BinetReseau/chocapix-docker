#!/bin/sh
docker build -t binetreseau/bars .
docker run --name="bars-db" -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=django -d mysql
docker run -p 8000:8000 --name="bars" --link="bars-db:mysqldb" binetreseau/bars
