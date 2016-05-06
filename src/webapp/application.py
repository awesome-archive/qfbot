#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin

import tornado.web
import motor
import tornadoredis

from .handler import urls
from . import setting


class Application(tornado.web.Application):

    def __init__(self):
        settings = dict(
            cookie_secret=setting.COOKIE_STR,
            template_path=setting.TEMPLATE,
            static_path=setting.STATIC,
            login_url="/login",
            debug=setting.DEBUG
        )

        super(Application, self).__init__(urls, **settings)
        self.db = motor.MotorClient(setting.MONGO_URI)[setting.MONGO_DB]
        pool = tornadoredis.ConnectionPool(
            max_connections=100,
            wait_for_available=True,
            host='localhost',
            port=6379
        )
        self.rdc = tornadoredis.Client(connection_pool=pool)
