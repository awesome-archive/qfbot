#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2015-09-26 01:46 CST

# RABBIT_MQ
RQ_URL = "amqp://guest@localhost//"

# MONGODB
MONGODB_URI = "mongodb://localhost:27017/"
MONGODB_NAME = "qfbot"

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ITEM_PIPELINES = {
    'crawler.pipelines.MongoPipeline': 200,
}
DOWNLOAD_DELAY = 0.05

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}
