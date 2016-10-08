#!/usr/bin/env python
# coding: utf-8
# vim: set et sw=4 ts=4 sts=4 fenc=utf-8
# Author: YuanLin

from tornado import ioloop
from tornado import gen
import pika
# from stormed import Connection, Message
import logging
try:
    import cPickle as pickle
except:
    import pickle
from crawler.tools.db import conn
from crawler.dispather import CrawlerFactory
from webapp import setting
# from crawler.spider.pagecrawler import PageDirectSpider

def generate():
    """
    """
    # projects = conn.project.find({})
    urls = "http://book.douban.com"
    projects = {}
    spider = CrawlerFactory("RUN").create(projects)
    publish(spider)


def publish(obj):
    """
    """
    params = pika.URLParameters(setting.mq_urls)
    connection = pika.BlockingConnection(params)
    channel.basic_publish('test_exchange',
                      'test_routing_key',
                      pickle.dumps(obj),
                      pika.BasicProperties(content_type='text/plain',
                                           delivery_mode=1))
    connection.close()


if __name__ == "__main__":
    # conn = Connection(host="localhost")
    # conn.connect(gern)
    ioloop.PeriodicCallback(generate, 3000).start()
    ioloop.IOLoop.instance().start()

