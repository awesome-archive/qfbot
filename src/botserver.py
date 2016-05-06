#!/usr/bin/env python
# encoding: utf-8
# vim: set et sw=4 ts=4 sts=4 fenc=utf-8
# Author: YuanLin
# Date: 2015-01-30 23:06:33


from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from webapp.application import Application


def main():
    http_server = HTTPServer(Application())
    http_server.listen(8888)
    http_server.start()
    IOLoop.instance().start()

if __name__ == "__main__":
    main()
