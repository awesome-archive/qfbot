#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2015-09-26 01:54 CST

from pymongo.connection import MongoClient

from .. import settings


class MongodbCursor(object):

    def __init__(self):
        client = MongoClient(settings.MONGODB_URI)
        self._db = client[settings.MONGODB_NAME]

    @property
    def crawler(self):
        return self._db

    @property
    def project(self):
        return self._db['project']

    @property
    def rawdata(self):
        return self._db["rawdata"]

    @property
    def old(self):
        return self._db["old"]

    @property
    def sample(self):
        return self._db["sample"]

    @property
    def consumer(self):
        return self._db["consumer"]

    @property
    def linkbase(self):
        return self._db['linkbase']

    @property
    def user(self):
        return self._db["user"]

conn = MongodbCursor()

__all__ = ["conn"]
