#!/bin/bash

cp Dockerfile_webapp Dockerfile
docker build -t qfbot-webapp .

docker ps -a |grep "qfbot-webapp"|awk '{print $1}'|xargs docker rm -f

docker run -d --restart="always" --name="qfbot-webapp" -p $1:8888 qfbot-webapp

