#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2015-09-26 02:30 CST


from urlparse import (parse_qs, urlsplit, urlunsplit)
from urllib import urlencode
import datetime
from copy import deepcopy
from pprint import pprint


class MockBase(object):
    """Base class
    """

    @classmethod
    def merge(cls, dics):
        if not dics:
            return {}
        tmp = [{d.get("key"): d.get("value")} for d in dics]
        c = reduce(cls.updic, tmp)
        return c

    @classmethod
    def updic(cls, x, y):
        x.update(y)
        return x


class MockParams(MockBase):
    def __init__(self, url, params):
        self._seed = url
        self._params = params
        self._urls = self._mock()

    @property
    def urls(self):
        return self._urls

    def _mock(self):
        _dict, _list, _format, const = [], [], [], []
        for pm in self._params:
            print pm
            if pm['spec'] == 'CONST':
                _dict.append(pm)
            elif pm['spec'] == 'TIME':
                pm['value'] = self.__mock_time(pm.get("option"))
                if pm['value']:
                    _dict.append(pm)
            elif pm['spec'] == 'PAGE':
                pm['value'] = self.__mock_page(pm.get("option"))
                if pm['value']:
                    _list.append(pm)
            elif pm['spec'] == 'LIST':
                _list.append(pm)
            elif pm['spec'] == 'FORMAT':
                _urls = self.__mock_format(pm)
                return _urls

        if _format:
            _urls = self.__mock_format(_format)
            return _urls

        if _dict:
            const = [self.merge(_dict)]

        res = self._map(const, _list)

        if const:
            _urls = map(self.gen_url, res)
            return _urls
        return None

    def __mock_time(self, op):
        if not op:
            return None
        fm = op.get("_format")
        tm = datetime.datetime.utcnow()
        value = tm.strftime(fm)
        return value

    def __mock_page(self, option):
        if not option:
            return None
        _max = int(option.get("max_count"))
        vol = int(option.get("vol"))
        start = int(option.get("start"))
        values = [i for i in range(_max/vol) if i>=start]
        return values

    def _map(self, _const, _lists):
        tmp = []
        for lst in _lists:
            tmp = self._extend(_const, lst)
            _const = tmp
        return _const

    def _extend(self, _qry, _list):
        res = []
        _lsts = [{_list['key']:i} for i in _list["value"]]
        if not _qry:
            return _lsts
        for q in _qry:
            tmp = map(lambda x: self.updic(x, q), _lsts)
            tmp = deepcopy(tmp)
            res.extend(tmp)
        return res

    def __mock_format(self, params):
        dic = []
        lst = []
        if not isinstance(params, list):
            params = [params]
        for pm in params:
            option = pm.get("option")
            if option.get("_type") == "page":
                pm['value'] = self.__mock_page(option)
                lst.append(pm)
            elif option.get("_type") == "list":
                lst.append(pm)
            else:
                dic.append(pm)
        const = list(self.merge(dic))
        qry = self._map(const, lst)
        _urls = [self._seed.format(**q) for q in qry]
        return _urls

    def gen_url(self, params):

        scheme, netloc, path, q_str, fragment = urlsplit(self._seed)
        if not isinstance(params, dict):
            return self._seed
        query_params = parse_qs(q_str)
        query_params.update(params)
        new_qstr = urlencode(query_params, doseq=True)
        return urlunsplit((scheme, netloc, path, new_qstr, fragment))


if __name__ == "__main__":
    urls = "https://api.douban.com/v2/book/search"
    params = [{
        "key": "q",
        "value": "python",
        "spec": "CONST",
        "option": None
    },
        {
            "key": "java",
            "value": [1, 2, 3, 4, 5],
            "spec": "LIST",
            "option": None
        },
        {
            "key": "scala",
            "value": [11],
            "spec": "LIST",
            "option": None
        },
        {
            "key": "start",
            "value": None,
            "spec": "PAGE",
            "option": {
                "vol": 20,
                "max_count": 889,
                "start": 0
            }
        }]
    mock = MockParams(urls, params)
    pprint(mock.urls)
    print len(mock.urls)
