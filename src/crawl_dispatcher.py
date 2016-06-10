#!/usr/bin/env python
# coding: utf-8
# vim: set et sw=4 ts=4 sts=4 fenc=utf-8
# Author: YuanLin

from tornado import ioloop
from tornado import gen
import pika
import logging


def generate():
    """
    """

def publish():
    """
    """


if __name__ == "__main__":
    ioloop.PeriodicCallback(generate, 3000).start()
    ioloop.IOLoop.instance().start()

