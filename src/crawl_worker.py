#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2016-05-22 17:44 CST

import pika
from pika import exceptions
from pika.adapters import twisted_connection
from twisted.internet import defer, reactor, protocol,task


class CrawlerConsumer(object):

    def __init__(self):
        pass

    @defer.inlineCallbacks
    def connect(self):
        param = pika.ConnectionParameters()
        cc = protocol.ClientCreator(reactor, twisted_connection.TwistedProtocolConnection, param)
        d = cc.connectTCP('hostname', 5672)
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
    def run(self):
        pass


def main():
    CrawlerConsumer().consume()
    reactor.run()


if __name__ == "__main__":
    main()
