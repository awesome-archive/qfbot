#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2015-09-26 01:54 CST

from scrapy.spider import Spider
# from scrapy.http import Request
from scrapy.selector import Selector
# from urlparse import urljoin, urlparse, urlunparse
# from scrapy.exceptions import CloseSpider
# from scrapy.contrib.linkextractors.lxmlhtml import LxmlParserLinkExtractor

from scrapy import log
from ..items import create_item_class


class PageDirectSpider(Spider):
    item_class = 'PageItem'

    def __init__(self, tpl, **kwargs):
        self.name = tpl.name
        self.items = tpl.items
        self.section = tpl.section
        self.project = tpl.project
        self.box = tpl.box
        self.start_urls = tpl.urls
        super(PageDirectSpider, self).__init__(**kwargs)

    def parse(self, response):
        log.msg("status %d" % response.status, level=log.INFO)
        fields = [item['name'] for item in self.items]
        item_cls = create_item_class(self.item_class, fields)
        items = item_cls()
        docx = Selector(response)
        if self.section:
            docs = docx.xpath(self.section)
        else:
            docs = [docx]
        for doc in docs:
            for itm in self.items:
                if itm.method == "XPATH":
                    tmp = doc.xpath(itm.value).extract()
                else:
                    tmp = doc.css(itm.value).extract()
                items[itm.name] = tmp
            yield items
