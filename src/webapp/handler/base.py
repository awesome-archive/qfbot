#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin


import json
from tornado import web
from tornado import gen
import logging
from bson import json_util
from bson import ObjectId
import uuid
import random


class BaseHandler(web.RequestHandler):
    """Base Handler
    """
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)

    @property
    def db(self):
        return self.application.db

    @property
    def loader(self):
        return self.application.loader

    @property
    def rdc(self):
        return self.application.rdc

    @classmethod
    def gen_oid(cls):
        return str(ObjectId())

    @classmethod
    def random_str(cls, length=5):
        """
        :return:
        """
        if length > 32 or length < 1:
            raise ValueError("invalid length")
        return uuid.uuid4().get_hex()[:length]

    @classmethod
    def random_num(cls, length=5):
        """
        :param length:
        :return:
        """
        if length > 10 or length < 1:
            raise ValueError("invalid length")
        arr = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        return random.sample(arr, length)

    @web.asynchronous
    @gen.engine
    def get(self, *args, **kwargs):
        if not hasattr(self, '_get_'):
            raise web.HTTPError(405)
        self._get_(*args, **kwargs)

    @web.asynchronous
    @gen.engine
    def post(self, *args, **kwargs):
        if not hasattr(self, '_post_'):
            raise web.HTTPError(405)
        self._post_(*args, **kwargs)

    @web.asynchronous
    @gen.engine
    def put(self, *args, **kwargs):
        if not hasattr(self, '_put_'):
            raise web.HTTPError(405)
        self._put_(*args, **kwargs)

    @web.asynchronous
    @gen.engine
    def delete(self, *args, **kwargs):
        if not hasattr(self, '_delete_'):
            raise web.HTTPError(405)
        self._delete_(*args, **kwargs)


class ApiAuthBaseHandler(BaseHandler):

    def write_error(self, status_code, **kwargs):
        self.set_header("Content-Type", 'application/json')
        result = {'code': status_code, 'detail': self._reason}
        msg = json.dumps(result)
        self.write(msg)
        self.finish()

    def write_message(self, data):
        """
        :param data: Message object.
        :return:
        """
        # self.set_header("Content-Type", 'application/json')
        msg = json.dumps(data, default=json_util.default)
        self.write(msg)
        self.finish()

    def load_json(self):
        try:
            data = json.loads(self.request.body)
        except Exception, e:
            logging.error(e)
            raise web.HTTPError(400)
        return data

    @gen.engine
    def _authenticate(self, callback=None):
        token = self.request.headers.get("Token")
        if not token:
            raise web.HTTPError(403)
        user_id = yield gen.Task(self.rdc.get, token)
        if user_id:
            self.current_user = user_id
        else:
            raise web.HTTPError(403)
        if callback:
            callback(None)

    @web.asynchronous
    @gen.engine
    def get(self, *args, **kwargs):
        yield gen.Task(self._authenticate)
        BaseHandler.get(self, *args, **kwargs)

    @web.asynchronous
    @gen.engine
    def post(self, *args, **kwargs):
        yield gen.Task(self._authenticate)
        BaseHandler.post(self, *args, **kwargs)

    @web.asynchronous
    @gen.engine
    def put(self, *args, **kwargs):
        yield gen.Task(self._authenticate)
        BaseHandler.put(self, *args, **kwargs)

    @web.asynchronous
    @gen.engine
    def delete(self, *args, **kwargs):
        yield gen.Task(self._authenticate)
        BaseHandler.delete(self, *args, **kwargs)


class WebAuthBaseHandler(BaseHandler):

    @gen.engine
    def _authenticate(self, callback=None):
        token = self.request.headers.get("UID")
        if not token:
            raise web.HTTPError(403)
        user_id = yield gen.Task(self.rdc.get, token)
        if user_id:
            self.current_user = user_id
        else:
            raise web.HTTPError(403)
        if callback:
            callback(None)

    @web.asynchronous
    @gen.engine
    def get(self, *args, **kwargs):
        yield gen.Task(self._authenticate)
        BaseHandler.get(self, *args, **kwargs)

    @web.asynchronous
    @gen.engine
    def post(self, *args, **kwargs):
        yield gen.Task(self._authenticate)
        BaseHandler.post(self, *args, **kwargs)

    @web.asynchronous
    @gen.engine
    def put(self, *args, **kwargs):
        yield gen.Task(self._authenticate)
        BaseHandler.put(self, *args, **kwargs)

    @web.asynchronous
    @gen.engine
    def delete(self, *args, **kwargs):
        yield gen.Task(self._authenticate)
        BaseHandler.delete(self, *args, **kwargs)
