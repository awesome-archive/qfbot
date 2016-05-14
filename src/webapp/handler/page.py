#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2016-05-07 09:30 CST


from tornado import gen
from tornado import web
import logging
import json

from .base import BaseHandler, ApiAuthBaseHandler
from ..tools.authenticate import Authenticate
# from .. import setting


class IndexHandler(ApiAuthBaseHandler):

    @gen.engine
    def _authenticate(self, callback=None):
        token = self.get_secure_cookie("Token")
        if not token:
            self.redirect("/login")
            return
        user_id = yield gen.Task(self.rdc.get, token)
        user = yield gen.Task(self.db["user"].find_one, {"_id": user_id})
        if user:
            self.current_user = user_id
        else:
            self.redirect("/login")
            return
        if hasattr(self, "_role"):
            if user.get("role", 0) < self._role:
                self.redirect("/login")
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


class LoginHandler(BaseHandler):

    @gen.coroutine
    def authenticate(self):
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
    def get(self, *args, **kwargs):
        flag = yield self.authenticate()
        if flag:
            self.redirect("/")
        else:
            print args, kwargs
            values = {"errors": ""}
            values.update(kwargs)
            self.render("login.html")

    @web.asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
            ajax api: LOGIN.POST
        """
        try:
            data = json.loads(self.request.body)
        except Exception, e:
            logging.error(e)
            self.write({"code": 410, "detail": u"email or password error"})
            self.finish()
            return
        email = data.get("email", "")
        password = data.get("password")
        find = yield self.db['user'].find_one({"email": email})
        if not find:
            self.write({"code": 410, "detail": u"email or password error"})
            self.finish()
            return
        salt = find.get("salt")
        hash_pw = find.get("hash_pw")
        if Authenticate.check_password(salt, password, hash_pw):
            self.set_secure_cookie("Token", find.get("user_id"))
            self.write({"code": 200, "detail": "login success"})
            self.finish()
            return


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


class PasswordForgotHandler(BaseHandler):
    """
    API: 重置密码API
    """

    @web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """

    @web.asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """


page_routes = [
    (r"/login/?", LoginHandler),
    (r"/signup/?", SignupHandler),
    (r"/logout/?", LogoutHandler),
    (r"/password_reset/?", PasswordResetHandler),
    (r"/password_forget/?", PasswordForgotHandler),
    (r'/?', IndexHandler)
]
