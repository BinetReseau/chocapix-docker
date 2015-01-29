#!/bin/sh
docker build -t binetreseau/bars .
docker run --rm -p 8000:8000 binetreseau/bars
