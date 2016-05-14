#!/usr/bin/env python
# coding=utf-8
# vim: set et sw=4 ts=4 sts=4
# Author: YuanLin
# Created: 2016-05-04 22:29 CST


import hashlib


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
        _hash_pass = cls.encrypt(salt, raw_pass)
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

    @staticmethod
    def encrypt(salt, raw_pass):
        """
        :param salt:
        :param raw_pass:
        :return:
        """
        to_hash = salt.encode("utf-8") + raw_pass.encode("utf-8")
        hash_pw = hashlib.sha256(to_hash).hexdigest()
        return hash_pw
