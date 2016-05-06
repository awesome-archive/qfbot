#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2015-09-26 01:45 CST

"""
   任务完成后将任务发送到message-mq中.产生一个新的任务.
"""


from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from billiard import Process
from urlparse import urlparse
import cPickle as pickle

# from .tools.cache import rdc

class BootCrawler(Process):

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

    def run(self):
        self.setup()
        log.start()
        reactor.run()

    def _next_crawl(self, spider, box):
        if hasattr(spider, "next_tpl") and spider.next_tpl:
            if box == "SANDBOX":
                from .tasks import debug_crawler_sub
                debug_crawler_sub(spider.next_tpl)
            else:
                from .tasks import sub_crawler_task
                sub_crawler_task().delay(spider.next_tpl)
            return True
        else:
            self.__done_task(spider.project)
            return False

    def __done_task(self, name):
        """
           Done spider tasks
        """
