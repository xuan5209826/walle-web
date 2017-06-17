# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-06-14 16:00:23
    :author: wushuiyong@walle-web.io
"""
from flask.ext.login import LoginManager, login_required
from flask_restful import Resource

class SecurityResource(Resource):

    module = None
    controller = None
    action = None

    @login_required
    def get(self, *args, **kwargs):
        self.action = 'get'
        pass

    @login_required
    def post(self, *args, **kwargs):
        pass


class Base(Resource):
    def get(self):
        """
        fetch role list or one role

        :return:
        """
        return 'walle-web 2.0'
