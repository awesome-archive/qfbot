#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin

from .member import member_routes
from .page import page_routes
from .project import project_routes

urls = []
urls.extend(member_routes)
urls.extend(page_routes)
urls.extend(project_routes)

