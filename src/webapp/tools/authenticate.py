#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2016-05-04 22:29 CST


import hashlib


def _encrypt(salt, raw_pass):
    """
    :param salt:
    :param raw_pass:
    :return:
    """
    if not isinstance(salt, unicode):
        salt = u""
    if not isinstance(raw_pass, unicode):
        raise ValueError("invalid raw password type.")
    to_hash = str(salt) + raw_pass.encode("utf-8")
    hash_pw = hashlib.sha256(to_hash).hexdigest()
    return hash_pw


class Authenticate(object):
    """
    """

    @classmethod
    def check_password(cls, salt, raw_pass, hash_pass):
        """
        :param salt:
        :param raw_pass:
        :param hash_pass:
        :return:
        """
        print ">>>> raw pass"
        print raw_pass
        print ">>>> hashed pass"
        print hash_pass
        print ">>>> salt"
        print salt
        _hash_pass = _encrypt(salt, raw_pass)
        print ">>> __hashed pass"
        print _hash_pass
        if str(_hash_pass) == str(hash_pass):
            return True
        else:
            return False

    @classmethod
    def user_view(cls, user):
        """
        :param user:
        :return:
        """
