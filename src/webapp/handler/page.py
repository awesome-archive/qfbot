#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2016-05-07 09:30 CST


from .base import BaseHandler, ApiAuthBaseHandler
from .. import setting


from tornado import gen
from tornado import web
import uuid
from tornado import template

class LoginHandler(ApiAuthBaseHandler):

    @gen.coroutine
    def _authenticate(self):
        token = self.get_secure_cookie("Token")
        if not token:
            raise gen.Return(None)
        user_id = yield gen.Task(self.rdc.get, token)
        user = yield self.db['user'].find_one({"_id": user_id})
        if user:
            self.current_user = user_id
        else:
            raise gen.Return(None)
        if hasattr(self, "_role"):
            if user.get("role", 0) < self._role:
                raise gen.Return(None)
        raise gen.Return(True)

    @web.asynchronous
    @gen.coroutine
    def _get_(self, *args, **kwargs):
        flag = yield self._authenticate()
        if flag:
            self.redirect("/")
        else:
            print args, kwargs
            loader = template.Loader(setting.TEMPLATE)
            values = {"errors": ""}
            values.update(kwargs)
            self.render("login.html")
            html = loader.load("login.html").generate(**values)
            self.write(html)
            self.finish()

    @web.asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        """


class SignupHandler(BaseHandler):

    @web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        """
        """

    @web.asynchronous
    @gen.coroutine
    def _post_(self):
        """
        """


class LogoutHandler(ApiAuthBaseHandler):

    @web.asynchronous
    @gen.coroutine
    def _get_(self):
        token = self.get_secure_cookie("Token")
        yield gen.Task(self.rdc.delete, token)
        self.redirect("/")


class PasswordResetHandler(ApiAuthBaseHandler):
    """
    API: 重置密码API
    """

    @web.asynchronous
    @gen.coroutine
    def _post_(self):
        """
        :return:
        """

class IndexHandler(ApiAuthBaseHandler):

    @gen.engine
    def _authenticate(self, callback=None):
        token = self.get_secure_cookie("Token")
        if not token:
            self.redirect("/login")
            return
        user_id = yield gen.Task(self.rdc.get, token)
        user = yield self.db["user"].find_one({"_id": user_id})
        if user:
            self.current_user = user_id
        else:
            self.redirect("/login")
            return
        if hasattr(self, "_role"):
            if user.get("role", 0) < self._role:
                self.redirect("/")
                return
        if callback:
            callback(user)

    @web.asynchronous
    @gen.coroutine
    def _get_(self):
        user = yield gen.Task(self._authenticate)
        if not self.current_user:
            self.redirect("/login")
            return
        else:
            values = {
                "user": user
            }
            self.render("index.html", **values)



user_routes = [
    (r"/login/?", LoginHandler),
    (r"/signup/?", SignupHandler),
    (r"/logout/?", LogoutHandler),
    (r"/password_reset/?", PasswordResetHandler),
    (r'/?', IndexHandler)
]
