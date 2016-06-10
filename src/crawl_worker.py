#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2016-05-22 17:44 CST

import pika
from pika import exceptions
from scrapy.utils.project import get_project_settings
from scrapy.crawler import Crawler
from scrapy import log, signals
import cPickle as pickle
from billiard import Process
from pika.adapters import twisted_connection
from twisted.internet import defer, reactor, protocol,task


class CrawlerProcess(Process):

    def __init__(self, spider):
        Process.__init__(self)
        self.spider = spider

    def setup(self):
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.configure()
        crawler.signals.connect(self._next_crawl,
                                signal=signals.spider_closed)
        crawler.crawl(self.spider)
        crawler.start()


class CrawlerConsumer(object):

    def __init__(self):
        """
        """
        self.connect()

    def connect(self):
        param = pika.ConnectionParameters()
        cc = protocol.ClientCreator(reactor, twisted_connection.TwistedProtocolConnection, param)
        d = cc.connectTCP('127.0.0.1', 5672)
        d.addCallback(lambda protocol: protocol.ready)
        d.addCallback(self.run)


    def _on_connect_(self):
        """
        :return:
        """

    def _on_disconnect(self):
        """
        :return:
        """

    @defer.inlineCallbacks
    def consume(self):
        """
        :return:
        """

    @defer.inlineCallbacks
    def run(self, connection):
        channel = yield connection.channel()
        exchange = yield channel.exchange_declare(exchange="qfbot_exchange", type="topic")
        queue = yield channel.queue_declare(queue="qfbot_queue", auto_delete=False, exclusive=False)
        yield channel.queue_bind(exchange="qfbot_exchange", queue="qfbot_queue", routing_key="qfbot_key")
        yield channel.basic_qos(prefetch_count=1)
        queue_object, consumer_tag = yield channel.basic_consume(queue="qfbot_queue", no_ack=False)
        l = task.LoopingCall(self.crawl, queue_object)
        l.start(0.01)

    @defer.inlineCallbacks
    def crawl(self, queue_object):
        ch, method, properties, body = yield queue_object.get()
        if body:
            spider = pickle.load(body)
            t = CrawlerProcess(spider)
            log.start()
            t.setup()
        yield ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    CrawlerConsumer()
    reactor.run()


if __name__ == "__main__":
    main()
