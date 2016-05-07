#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2016-05-04 22:28 CST

import hashlib
from tornado import gen
from tornado.web import HTTPError
import json
from bson import json_util

from .base import ApiAuthBaseHandler


class MemberHandler(ApiAuthBaseHandler):

    @gen.coroutine
    def _get_(self):
        page_num = self.get_argument("page", default=0)
        u_id = self.get_argument("_id", default=None)
        res = {}
        if not u_id:
            cnt = yield self.user_count()
            user_list = yield self.list_user(page_num)
            res["count"] = cnt
            res['user'] = user_list
            self.write(json.dumps(res, default=json_util.default))
            self.finish()
        else:
            result = yield self.db["user"].find_one({"_id": u_id})
            self.write(json.dumps(result, default=json_util.default))
            self.finish()

    @gen.coroutine
    def user_count(self):
        count = yield self.db['user'].count()
        raise gen.Return(count)

    @gen.coroutine
    def list_user(self, page_num):
        cursor = (self.db['user'].find()
                  .skip(int(page_num)*20)
                  .limit(50))
        result = yield cursor.to_list(50)
        raise gen.Return(result)

    @gen.coroutine
    def post(self, *args, **kwargs):
        try:
            data = json.loads(self.request.body)
        except ValueError:
            raise HTTPError(400)
        if not data:
            raise HTTPError(400)
        message = {}

        create_data = data.get('CREATE')
        if create_data:
            message = yield self.bulk_create(create_data)

        update_data = data.get('UPDATE')
        if update_data:
            message = yield self.bulk_update(update_data)

        delete_data = data.get('DELETE')
        if delete_data:
            message = yield self.bulk_delete(delete_data)

        if not message:
            message = {'code': 403, 'detail': u'permission denied'}
        self.write(json.dumps(message, default=json_util.default))
        self.finish()

    @gen.coroutine
    def bulk_create(self, data):
        try:
            email = data.get('email')
        except KeyError:
            raise HTTPError(400)
        if "password" in data:
            hash_pw = hashlib.sha1(data.pop("password")).hexdigest()
            data['hash_pw'] = hash_pw
        result = yield self.db['user'].find_one({'email': email})
        if result:
            msg = {'code': 302, 'detail': "email exists"}
            raise gen.Return(msg)
        r = yield self.db['user'].insert(data)
        if r:
            msg = {'code': 200, 'detail': "create finished"}
            raise gen.Return(msg)

    @gen.coroutine
    def bulk_update(self, data):
        u_id = data.pop('_id')
        if not u_id:
            raise HTTPError(400)
        if "password" in data:
            hash_pw = hashlib.sha1(data.pop("password")).hexdigest()
            data['hash_pw'] = hash_pw
        if not isinstance(data, dict):
            raise HTTPError(400)
        yield self.db['user'].update(
            {"_id": u_id}, {"$set": data}, upsert=True)
        msg = {'code': 200, 'detail': "update finished"}
        raise gen.Return(msg)

    @gen.coroutine
    def bulk_delete(self, data):
        u_id = data.get('_id')
        if not isinstance(data, dict):
            raise HTTPError(400)
        yield self.db['user'].remove({"_id": u_id})
        msg = {'code': 200, 'detail': "delete finished"}
        raise gen.Return(msg)

member_routes = [
    (r'/member/?', MemberHandler),
]
