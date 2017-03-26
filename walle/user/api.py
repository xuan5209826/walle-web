# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-25 11:15:01
    :author: wushuiyong@walle-web.io
"""


import math
from flask import Blueprint, request

from walle.common import models
from walle.common.controller import Controller
from walle.user.forms import RegistrationForm
from flask.ext.restful import reqparse, abort, Api, Resource

api_blue_bp = Blueprint('v2', __name__, static_folder='assets')
controller = Controller()

@api_blue_bp.route('/role/', methods=['GET', 'POST'])
@api_blue_bp.route('/role/list', methods=['GET', 'POST'])
def role_list():
    page = int(request.args.get('page', 0))
    page = page - 1 if page else 0
    size = float(request.args.get('size', 2))
    kw = request.values.get('kw', '')

    role_model = models.Role()
    role_list = role_model.list(page=page, size=size, kw=kw)
    return controller.render_json(data=role_list, count=13)


@api_blue_bp.route('/role/item', methods=['GET', 'POST'])
def role_item():
    role_id = request.args.get('role_id', 0)
    role_model = models.Role()
    if role_id:
        role_info = role_model.item(role_id)
        return controller.render_json(data=role_info)

    return controller.render_json()


