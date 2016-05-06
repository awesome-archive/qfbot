#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2015-09-26 02:47 CST

import datetime
from copy import deepcopy


class Template(object):

    def dumps(self):
        """
        """

    def generate(self):
        """
        """


class SpiderTemplate(object):
    def __init__(self, urls, box, name, project, items, section,
                 offset, parse, queue, point=None, setting=None):
        self.urls = urls
        self.box = box
        self.name = name
        self.project = project
        self.items = items
        self.section = section
        self.offset = offset
        self.point = point
        self.parse = parse
        self.queue = queue
        self.setting = setting
        self.created = datetime.datetime.utcnow()


class Param(Template):
    allow_spec = ('TIME_NOW', 'CONST', 'LIST', 'PAGE', 'PAGE_VOL', "FORMAT")

    def __init__(self, key, value, spec="CONST", default=None,
                 volume=None, start=0, max_count=20, fmt=""):
        self._key = key
        self._value = value
        self._spec = spec
        self._default = default
        self._vol = volume
        self._start = start
        self._max_count = max_count
        self._fmt = fmt

    def dumps(self):
        return {
            "key": self._key,
            "value": self._value,
            "options": {
                "default": self._default,
                "vol": self._vol,
                "spec": self._spec,
                "fmt": self._fmt,
                "max_count": self._max_count,
                "start": self._start
            }
        }

    def generate(self):
        if isinstance(self._value, list):
            return [{self._key: d} for d in self._value]
        if not self._value:
            value = self._default
        else:
            value = self._value
        if self._spec == "CONST":
            return {self._key: value}
        if self._spec == "FORMAT":
            return {self._key: value}
        if self._spec == "PAGE":
            return self.__pagination()
        if self._spec == "TIME_NOW":
            return self.__time()

    def __pagination(self):
        return [{self._key: i} for i in range(self._max_count/self._vol) if i >= self._start]

    def __time(self):
        tm = datetime.datetime.utcnow()
        value = tm.strftime(self._fmt)
        return {self._key: value}

    @property
    def spec(self):
        return self._spec


class Payload(Template):
    def __init__(self, params):
        self._items = []
        self._item_list = []
        self._item_const = []
        self._item_format = None
        for p in params:
            op = deepcopy(p.get("options"))
            if not isinstance(op, dict):
                raise ValueError("param.options should be dict type")
            p_obj = Param(p['key'], p.get("value"), **op)
            self._items.append(p_obj)

    def dumps(self):
        res = []
        for item in self._items:
            res.append(item.dumps())
        return res

    def generate(self):
        for p in self._items:
            if isinstance(p.spec, list):
                self._item_list.append(p.generate())
            elif p.spec == "PAGE" or p.spec == "PAGE_VOL":
                self._item_list.append(p.generate())
            elif p.spec == "FORMAT":
                self._item_format = p.generate()
            else:
                self._item_const.append(p.generate())


class Headers(Template):
    """
    """


class Setting(Template):
    """
    """


class Items(Template):
    """
    """


class Status(Template):
    """
    """


class Crawler(Template):
    """
    """
    allow_box = ("PRODUCTION", "SANDBOX")
