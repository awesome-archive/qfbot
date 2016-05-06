#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2015-09-26 01:45 CST

"""
    USAGE:

        celery -A crawler worker -B -Q sandbox --loglevel=INFO
"""

from __future__ import absolute_import
from celery import Celery
from celery.schedules import crontab
# from . import conf


crawler = Celery(
    "crawler",
    broker="",
    backend='amqp',
    include=[
        "crawler.tasks",
    ])

crawler.conf.update(
    CELERY_ROUTES={
        'crawler.tasks.debug_crawler_task': {'queue': 'sandbox'},
        'crawler.tasks.debug_crawler_sub': {'queue': 'sandbox'},
    },
    # heart beat
    CELERYBEAT_SCHEDULE={
        "heart_beat": {
            "task": "crawler.tasks.heat_beat",
            "schedule": crontab(minute=10, hour=0),
            "args": ()
        },
    },
    CELERY_TIMEZONE='UTC'
)


if __name__ == "__main__":
    crawler.start()
