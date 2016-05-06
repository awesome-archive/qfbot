#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2015-09-26 01:45 CST


from __future__ import absolute_import
import datetime

from .celery import crawler
from . import settings
from . import dispatcher


@crawler.task
def debug_crawler_task(project):
    """
    """
    schema = dispatcher.CrawlerHandler.get_project(project)
    ctx = dispatcher.CrawlerHandler(schema).debug()
    if ctx.err:
        err = ctx.err
        return err
    debug_crawler = dispatcher.CrawlerFactory("SANDBOX").crawl(ctx.head, ctx.tpls)
    debug_crawler.run()


@crawler.task
def debug_crawler_sub(tpl):
    debug_tpl = dispatcher.CrawlerFactory("SANDBOX")


@crawler.task
def heart_beat():
    """
    :return:
    """


@crawler.task
def crawler_task(task_id, tpl):
    """
    :param tpl:
    :return:
    任务过程中产生的link，使用task_id的方式存储到redis中，然后进行下一步抓取
    """
