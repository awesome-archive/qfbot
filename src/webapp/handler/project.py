#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2016-05-04 22:28 CST


from bson import json_util
from tornado.web import HTTPError
import json
import datetime
import logging
from tornado import gen
from tornado import web

# from ..model import doc
from .base import ApiAuthBaseHandler


class ProjectHandler(ApiAuthBaseHandler):

    @web.asynchronous
    @gen.coroutine
    def _get_(self):
        project_id = self.get_argument("project_id", None)
        _type = self.get_argument("_type", None)
        next_id = self.get_argument("next_id", None)
        if project_id:
            project = yield self.db["project"].find_one({"_id": project_id})
            self.write_message({"code": 200, "detail": project})
            return
        else:
            query = {}
            if _type:
                query.update({"_type": _type})
            if next_id:
                query.update({"_id": {"$lte": next_id}})
            projects = yield self.db["project"].find(query)
            count = projects.count()

    @web.asynchronous
    @gen.coroutine
    def _post_(self):
        """
        :return:
        """
        try:
            _dat = json.loads(self.request.body)
        except ValueError, e:
            logging.error(e)
            self.write_message({"code": 400, "detail": "error data type"})
            return

    @web.asynchronous
    @gen.coroutine
    def _put_(self):
        """
        :return:
        """

    @web.asynchronous
    @gen.coroutine
    def _delete_(self):
        """
        :return:
        """


project_routes = [
    (r'/project/?', ProjectHandler),
]
