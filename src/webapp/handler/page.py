#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2016-05-07 09:30 CST


from tornado import gen
from tornado import web
import logging
import json

from .base import BaseHandler, ApiAuthBaseHandler, WebAuthBaseHandler
from ..tools.authenticate import Authenticate
# from .. import setting


class IndexHandler(WebAuthBaseHandler):

    @web.asynchronous
    @gen.coroutine
    def _get_(self):
        user = self.current_user
        values = user
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
        password = data.get("password", "")
        find = yield self.db['user'].find_one({"email": email})
        logging.error(find)
        if not find:
            self.write({"code": 410, "detail": u"email or password error"})
            self.finish()
            return
        salt = find.get("salt")
        hash_pw = find.get("password")
        try:
            flag = Authenticate.check_password(salt, password, hash_pw)
        except ValueError, e:
            logging.error(e)
            self.write({"code": 410, "detail": u"email or password error"})
            self.finish()
            return
        if flag:
            self.set_secure_cookie("Token", find.get("_id"))
            self.write({"code": 200, "detail": "login success"})
            self.finish()
            return
        else:
            self.write({"code": 410, "detail": u"email or password error"})
            self.finish()
            return


class SignupHandler(BaseHandler):

    @web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):

        self.render("signup.html")

    @web.asynchronous
    @gen.coroutine
    def _post_(self):

        try:
            data = json.loads(self.request.body)
        except Exception, e:
            logging.error(e)
            self.write({"code": 410, "detail": u"signup failed"})
            self.finish()
            return
        logging.error(data)

class SignupSucceedHandler(BaseHandler):

    @web.asynchronous
    @gen.coroutine
    def get(self):
        self.render("signup_succeed.html")


class LogoutHandler(WebAuthBaseHandler):

    @web.asynchronous
    @gen.coroutine
    def _get_(self):
        self.clear_all_cookies()
        logging.error("login success")
        self.redirect("/login")


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

class ProjectPageHandler(WebAuthBaseHandler):
    """
    WEB: project的页面
    """

    @web.asynchronous
    @gen.coroutine
    def _get_(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        user = self.current_user
        values = user
        self.render("project.html", **values)

page_routes = [
    (r"/login/?", LoginHandler),
    (r"/signup/?", SignupHandler),
    (r"/logout/?", LogoutHandler),
    (r"/password_reset/?", PasswordResetHandler),
    (r"/password_forget/?", PasswordForgotHandler),
    (r'/?', IndexHandler),
    (r'/project/?', ProjectPageHandler),
    (r'/signup_succeed/?', SignupSucceedHandler),
]
