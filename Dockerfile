FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y python-dev python-pip libxml2-dev libxslt-dev
RUN apt-get install -y zlib1g-dev
RUN apt-get install -y libffi-dev
RUN apt-get install -y libssl-dev
RUN pip install lxml tornado twisted redis pika scrapy service-identity motor

