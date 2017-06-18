# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-06-14 16:00:23
    :author: wushuiyong@walle-web.io
"""
import logging

from flask import jsonify
from flask.ext.login import login_required
from flask_restful import Resource
from walle.service.rbac.access import Access as AccessRbac


class ApiResource(Resource):
    module = None
    controller = None
    action = None

    @staticmethod
    def render_json(code=0, message='', data=[]):
        return jsonify({
            'code': code,
            'message': message,
            'data': data,
        })

    @staticmethod
    def json(code=0, message=None, data=[]):
        return jsonify({
            'code': code,
            'message': message,
            'data': data,
        })

    @staticmethod
    def list_json(list, count, code=0, message=''):
        return ApiResource.render_json(data={'list': list, 'count': count}, code=code, message=message)


class SecurityResource(ApiResource):
    module = None
    controller = None
    action = None

    @login_required
    def get(self, *args, **kwargs):
        self.action = 'get'
        resource = AccessRbac.resource(action=self.action, controller=self.controller)
        logging.error(resource)
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
