#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2015-09-26 01:46 CST


from scrapy.item import DictItem, Field


def create_item_class(class_name, field_list):
    fields = {field_name: Field() for field_name in field_list}
    return type(class_name, (DictItem, ), {'fields': fields})
