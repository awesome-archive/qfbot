#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2015-09-26 01:47 CST

"""
    分布式pub-sub的爬虫管理.

    运行spider之前，需要制定其url pool
    以及制定其spider对象.

        LIST    ListSpider
        NEWS    NewsListSpider
        DETAIL  DetailSpider
        SRP     SRPBuildSpider
        XML     XMLSpider
        JSON    APISpider
        PAGE    PageDirectSpider
        BOARD   BoardSpider
"""

import cPickle as pickle
import uuid
import logging
from copy import deepcopy

from .spiders.pagecrawler import PageDirectSpider
from .boot import BootCrawler
from .items import create_item_class
from .util.template import Template
from .tools.db import conn
from .tools import rdc


class TaskPool(object):

    def create(self):
        """
        :return:
        """


class CrawlerTask(object):

    @classmethod
    def cset(cls, obj):
        if not obj:
            print ">>> no active spider object"
            return False
        p_obj = pickle.dumps(obj)
        r = rdc.conn.rset(obj.name, p_obj)
        return r

    @classmethod
    def cget(cls, name):
        qry = rdc.conn.get(name)
        p_obj = pickle.loads(qry)
        return p_obj

    @classmethod
    def get_key(cls, _model, proc, box, name):
        fmt = {
            "model": _model,
            "proc": proc,
            "box": box,
            "name": name
        }
        key = "{model}::{proc}::{box}::{name}".format(**fmt)
        return key


class CrawlerFactory(object):
    def __init__(self, box):
        self.box = box

    def _create_item(self, tpl):
        """
        :return:
        """

    def create(self, tpl):
        if tpl.chain == "LIST":
            return self._creat_list(tpl)
        elif tpl.chain == "DETAIL":
            return self._create_detial(tpl)
        elif tpl.chain == "PAGE":
            return self._create_page(tpl)
        elif tpl.chain == "XML":
            return self._create_xml(tpl)
        elif tpl.chain == "JSON":
            return self._create_api(tpl)
        elif tpl.chain == "SRP":
            return self._create_srp(tpl)
        elif tpl.chain == "NEWS":
            return self._create_news(tpl)
        else:
            return False

    def _creat_list(self, tpl):
        return tpl

    def _create_detial(self, tpl):
        return tpl

    def _create_srp(self, tpl):
        return tpl

    def _create_api(self, tpl):
        return tpl

    def _create_xml(self, tpl):
        return tpl

    def _create_news(self, tpl):
        """
        :param tpl:
        :return:
        """

    def _create_page(self, tpl):
        spider = PageDirectSpider(tpl, self.box)
        return spider

    def crawl(self, head, tpls):
        print ">>>>>", head.urls
        head_spider = self.create(head)
        print ">>>", head_spider
        for tpl in tpls:
            print ">>> ++++ add tpls"
            spider = self.create(tpl)
            CrawlerTask.cset(spider)
        crawltask = BootCrawler(head_spider)
        return crawltask


class CrawlerHandler(object):
    """"""
    def __init__(self, data):
        self.data = data
        self.project = data.get("project")

    @classmethod
    def get_status(cls, name):
        find = conn.crawler['status'].find_one({"project": name})
        return find

    @classmethod
    def get_project(cls, name, bucket="SANDBOX"):
        find = conn.crawler['production'].find_one({"project": name, "bucket": bucket})
        return find

    @classmethod
    def set_status(cls, data, proc):
        """"""
        status = {
            "project": data.get("project"),
            "beat": data.get("beat"),
            "source": data.get("source"),
            "_type": data.get("_type"),
            "proc": proc
        }
        return status

    @classmethod
    def set_template(cls, raw_tpl):
        """
        """

    @classmethod
    def gen_key(cls, _model):
        """
        :param _model:
        :return:
        """

    def run(self):
        """
        :return:
        """

    def debug(self):
        """
        :return:
        """
