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
from flask.ext.login import current_user
from flask.ext.login import login_user
from walle.user.forms import RegistrationForm, LoginForm
bp_api = Blueprint('v2', __name__, static_folder='assets')
controller = Controller()
from walle.common.models import db
from werkzeug.security import check_password_hash,generate_password_hash

@bp_api.route('/role/', methods=['GET'])
def role_list():
    """
    获取角色列表

    :return:
    """
    page = int(request.args.get('page', 0))
    page = page - 1 if page else 0
    size = float(request.args.get('size', 10))
    kw = request.values.get('kw', '')

    role_model = models.Role()
    role_list = role_model.list(page=page, size=size, kw=kw)
    return controller.render_json(data=role_list, count=13)


@bp_api.route('/role/<int:role_id>', methods=['GET'])
def role_item(role_id):
    """
    获取某角色

    :param role_id:
    :return:
    """
    role_model = models.Role()
    if role_id:
        role_info = role_model.item(role_id)
        return controller.render_json(data=role_info)

    return controller.render_json()


@bp_api.route('/role/', methods=['POST'])
def role_create():
    """
    新增角色

    :return:
    """
    role_name = request.form.get('role_name', None)
    role_permissions_ids = request.form.get('permissions_ids', '')
    role_model = models.Role()
    ret = role_model.add(name=role_name, permission_ids=role_permissions_ids)
    return controller.render_json(code=ret)


@bp_api.route('/role/<int:role_id>', methods=['PUT'])
def role_update(role_id):
    """
    修改角色

    :param role_id:
    :return:
    """
    role_name = request.args.get('role_name', 0)
    role_permissions_ids = request.args.get('permissions_ids', 0)

    if not role_name:
        return controller.render_json(code=-1, message='role_name can not be empty')
    role_model = models.Role()
    ret = role_model.update(role_id, role_name, role_permissions_ids)
    return controller.render_json(code=ret)


@bp_api.route('/role/<int:role_id>', methods=['DELETE'])
def role_remove(role_id):
    """
    删除一个角色

    :return:
    """
    role_model = models.Role()
    ret = role_model.remove(role_id)

    return controller.render_json(code=ret)


@bp_api.route('/passport/signin', methods=['POST'])
def signin():

    form = LoginForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return controller.render_json(data={'user_info': current_user.to_json()})

    return controller.render_json(code=-1, data=form.errors)


@bp_api.route('/passport/signup', methods=['POST'])
def signup():
    form = RegistrationForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        user = models.User(email=form.email.data,
                    username=form.email.data,
                    password=password)
        db.session.add(user)
        db.session.commit()
        return controller.render_json(data={'user_id':user.id, 'oldpwd': password,'password':generate_password_hash(form.password.data)})
        return redirect(url_for('passport.signin'))
    return controller.render_json(code=-1, message='todo')


    user = User()
    done = user.add(email=request.form.get('email'), password=request.form.get('password'))
    return controller.render_json(data=done)
    code = -1 if done else 0
    return controller.render_json(code=code, data=done)


@bp_api.route('/group/', methods=['GET'])
def group_list():
    """
    用户组列表

    :return:
    """
    page = int(request.args.get('page', 0))
    page = page - 1 if page else 0
    size = float(request.args.get('size', 10))
    kw = request.values.get('kw', '')

    group_model = models.Group()
    group_list = group_model.list(page=page, size=size, kw=kw)
    return controller.render_json(data=group_list, count=13)


@bp_api.route('/group/<int:group_id>', methods=['GET'])
def group_item(group_id):
    """
    获取某个用户组

    :param group_id:
    :return:
    """

    group_model = models.Group()
    group_info = group_model.item(group_id)
    return controller.render_json(data=group_info)


@bp_api.route('/group/', methods=['POST'])
def group_create():
    """
    添加用户组

    :return:
    """
    user_ids = request.form.get('user_ids', '')
    group_name = request.form.get('group_name', None)

    if user_ids and group_name:
        group_model = models.Group()

        ret = group_model.add(group_name=group_name, user_ids=user_ids)
        return controller.render_json(data=ret, message=user_ids)
    else:
        return controller.render_json(code=-1, message='group_name can not be empty')


@bp_api.route('/group/<int:group_id>', methods=['PUT'])
def group_update(group_id):
    """
    添加用户组

    :return:
    """
    user_ids = request.form.get('user_ids', '')
    user_ids = [int(i) for i in user_ids.split(',')]
    group_name = request.form.get('group_name', None)
    if user_ids and group_name:
        group_model = models.Group()
        group_info = group_model.update(group_id=group_id, group_name=group_name, user_ids=user_ids)
        return controller.render_json(data=group_info)

    return controller.render_json()

@bp_api.route('/group/<int:group_id>', methods=['DELETE'])
def group_remove(group_id):
    group_model = models.Group()
    tag_model = models.Tag()
    tag_model.remove(group_id)


    return controller.render_json(message='')
