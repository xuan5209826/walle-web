# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-06-11 15:40:38
    :author: wushuiyong@walle-web.io
"""


class Access:
    def __init__(self):
        pass

    def is_allow(self, resource, method):
        return True

    @staticmethod
    def resource(action, controller, module=None):
        return "{}_{}_{}".format(module, controller, action)
