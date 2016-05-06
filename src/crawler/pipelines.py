#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2015-09-26 01:46 CST


from scrapy import log
# import datetime
# import re
# import json
# import codecs
# # from pyes import ES
# import hashlib
# # import types

from .tools.db import conn


class MongoPipeline(object):
    """Mongodb pipelines"""

    def process_item(self, item, spider):
        # debug flag
        if spider.mode == "DEBUG":
            mongo = conn.sample
        else:
            mongo = conn.rawdata
        if not item:
            return item

        # support items
        qfbot_item = {
        }

        find = mongo.find_one({"href": qfbot_item.get("href")})
        if find:
            mongo.update({"href": qfbot_item.get("href")},
                         {"$set": qfbot_item}, upsert=True)
            log.msg('update %s' % qfbot_item.get("href"), level=log.INFO)
            return item
        else:
            mongo.save(qfbot_item)
            return item
