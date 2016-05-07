#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2016-05-07 09:30 CST


import hashlib
from tornado import gen
from tornado import web
from tornado.web import HTTPError
import json
from bson import json_util

from .base import WebAuthBaseHandler
from .base import BaseHandler


class LoginPageHandler(BaseHandler):
    """
    """

    @web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        """
        """


class IndexPageHandler(WebAuthBaseHandler):
    """
    """

    @gen.coroutine
    def authenticate(self):
        """
        """

    @web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
