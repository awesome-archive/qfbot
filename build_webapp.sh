#!/bin/bash

cp Dockerfile_webapp Dockerfile

docker build -t qfbot-base/webapp .