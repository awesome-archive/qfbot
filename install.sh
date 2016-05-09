#!/bin/bash

apt-get update -qq
apt-get install -y g++
apt-get install -y libxml2-dev libxslt-dev python-dev python-pip
pip install lxml
pip install -r requirements.pip