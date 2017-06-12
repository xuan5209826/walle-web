# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-06-11 15:40:38
    :author: wushuiyong@walle-web.io
"""
from walle.common import models


class Access:
    def __init__(self):
        pass

    def get_menu(self):
        menu = models.Access().menu('x')

        return menu

    def is_allow(self, resource, method):
        return True
