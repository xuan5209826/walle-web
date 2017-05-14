# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-12 17:08:38
    :author: wushuiyong@walle-web.io
"""
from flask import jsonify

class Controller:
    @staticmethod
    def render_json(code=0, message='', data=[], count=0):
        return jsonify({
            'code': code,
            'message': message,
            'data': data,
        })

    @staticmethod
    def json(code=0, message=None, data=[], count=0):
        return jsonify({
            'code': code,
            'message': message,
            'data': data,
        })

    @staticmethod
    def list_json(list, count):
        return Controller.render_json(data={'list': list, 'count': count})

