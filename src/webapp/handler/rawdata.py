#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2016-05-04 22:28 CST

import datetime
from tornado.gen import coroutine
from tornado import gen
from tornado.web import HTTPError
import json
from bson.code import Code
from bson import json_util

from .base import ApiAuthBaseHandler


class DataHandler(ApiAuthBaseHandler):

    @coroutine
    def _get_(self):
        status = self.get_argument("status", default=None)
        category = self.get_argument("category", default=None)
        page_num = self.get_argument("page", default=0)
        tm = self.get_argument("time", default=None)
        project = self.get_argument("project", default=None)

        if status == 'all':
            status_code = 'ALL'
        elif status == "pass":
            status_code = 1
        elif status == "fail":
            status_code = "fail"
        else:
            status_code = None
        if category == 'null':
            category = None
        td = datetime.date.today()
        dt = datetime.datetime(td.year, td.month, td.day)
        if tm == "today":
            dates = {"updated": {"$gte": dt}}
        elif tm == "older":
            dates = {"updated": {"$lt": dt}}
        else:
            dates = None

        result = yield self.get_posts(category, status_code, page_num, project, dates)
        if not (status_code or category or tm or project or dates):
            cnts = yield self.group_prj()
            result["total"] = cnts

        message = json.dumps(result, default=json_util.default)
        self.write(message)
        self.finish()

    @coroutine
    def get_posts(self, category, status, page_num, project, qtime):
        query = {"expired": None}

        if status != "ALL":
            if status == "fail":
                status = 0
            query.update({"status": status})
        if category:
            query.update({"category": category})
        if project:
            query.update({"source": project})
        if qtime:
            query.update(qtime)
        cursor = (self.db["rawdata"].find(query)
                  .skip(int(page_num)*10)
                  .limit(10))

        res = yield cursor.to_list(10)
        cnts = yield self.db["rawdata"].find(query).count()
        result = {"data": res, "total": cnts}
        raise gen.Return(result)

    @coroutine
    def _post_(self):
        data = json.loads(self.request.body)
        if not data:
            raise HTTPError(400)
        message = {}
        update_data = data.get('UPDATE')
        status = data.get('STATUS')
        if update_data:
            message = yield self.bulk_update(update_data)

        if status:
            message = yield self.modify_status(status)

        if not message:
            raise HTTPError(400)
        self.write(json.dumps(message, default=json_util.default))
        self.finish()

    @coroutine
    def bulk_update(self, data):
        if not isinstance(data, dict):
            raise HTTPError(400)
        p_id = data.pop("_id")
        oid = self.validate_id(p_id)
        if oid:
            result = yield self.db['rawdata'].update({"_id":oid}, {'$set':data})
            if result.get('updatedExisting'):
                msg = {"code": 200, "msg": "update succeed"}
                raise gen.Return(msg)
            raise gen.Return({"code": 302, "detail": "update failed"})
        else:
            raise HTTPError(400)

    @coroutine
    def modify_status(self, status):
        """Modify status
        """
        p_id = status.pop("_id")
        oid = self.validate_id(p_id)
        if status["status"] == 1:
            result = yield self.db['rawdata'].find_one({"_id": oid})
            user = self.current_user['email']
            result.update({"email": user, "data-source": "crawl"})
            json_str = json.dumps(result, default=json_util.default)
            self.rdc.sadd("crawl:rawdata", json_str)

        if oid:
            result = yield self.db['rawdata'].update(
                {"_id": oid}, {"$set": status})
            if result.get('updatedExisting'):
                msg = {"code": 200, "msg": "update succeed"}
                raise gen.Return(msg)
            print result

            raise gen.Return({"code": 302, "detail": "update failed"})
        else:
            raise HTTPError(400)

    @gen.coroutine
    def group_prj(self):
        reducer = Code(
            """
                function(obj, prev){
                    prev.count++;
                }
            """
        )
        results = yield self.db['rawdata'].group(
            key={"source"}, condition={'expired': None},
            initial={"count": 0}, reduce=reducer)
        r = {}
        for doc in results:
            d = doc.get('source')
            r[d] = doc.get('count')
        raise gen.Return(r)
