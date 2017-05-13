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
from walle.user.forms import RegistrationForm, UserUpdateForm, GroupForm, EnvironmentForm
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.ext.login import current_user
from flask.ext.login import login_user
from walle.user.forms import RegistrationForm, LoginForm

bp_api = Blueprint('v2', __name__, static_folder='assets')
controller = Controller()
from walle.common.models import db
from werkzeug.security import check_password_hash, generate_password_hash


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
        return controller.render_json(
                data={'user_id': user.id, 'oldpwd': password, 'password': generate_password_hash(form.password.data)})
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

    group_model = models.Group(group_id=group_id)
    group_info = group_model.item()
    return controller.render_json(data=group_info)


@bp_api.route('/group/', methods=['POST'])
def group_create():
    """
    添加用户组

    :return:
    """

    form = GroupForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        user_ids = [int(uid) for uid in form.user_ids.data.split(',')]

        group_new = models.Group()
        ret = group_new.add(group_name=form.group_name.data, user_ids=user_ids)
        return controller.render_json(data=ret, message=user_ids)
    else:
        return controller.render_json(code=-1, message=form.errors)


@bp_api.route('/group/<int:group_id>', methods=['PUT'])
def group_update(group_id):
    """
    修改用户组

    :return:
    """
    form = GroupForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        user_ids = [int(uid) for uid in form.user_ids.data.split(',')]

        group_model = models.Group(group_id=group_id)
        group_info = group_model.update(group_id=group_id,
                                        group_name=form.group_name.data,
                                        user_ids=user_ids)
        return controller.render_json(data=group_info)

    return controller.render_json(code=-1,message=form.errors)


@bp_api.route('/group/<int:group_id>', methods=['DELETE'])
def group_remove(group_id):
    group_model = models.Group()
    tag_model = models.Tag()
    tag_model.remove(group_id)
    group_model.remove(group_id)

    return controller.render_json(message='')


@bp_api.route('/user/', methods=['GET'])
def user_list():
    """
    用户列表

    :return:
    """
    page = int(request.args.get('page', 0))
    page = page - 1 if page else 0
    size = float(request.args.get('size', 10))
    kw = request.values.get('kw', '')

    user_model = models.User()
    user_list = user_model.list(page=page, size=size, kw=kw)
    return controller.render_json(data=user_list, count=13)


@bp_api.route('/user/<int:user_id>', methods=['GET'])
def user_item(user_id):
    """
    获取某个用户

    :param user_id:
    :return:
    """

    user_info = models.User(id=user_id).item()
    return controller.render_json(data=user_info)


@bp_api.route('/user/', methods=['POST'])
def user_create():
    """
    添加用户

    :return:
    """
    form = RegistrationForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        user = models.User(email=form.email.data,
                           username=form.username.data,
                           password=password,
                           role_id=form.role_id.data
                           )
        db.session.add(user)
        db.session.commit()
        return controller.render_json(data=user.item())
    return controller.render_json(code=-1, message=form.errors)


@bp_api.route('/user/<int:user_id>', methods=['PUT'])
def user_update(user_id):
    """
    编辑用户

    :return:
    """
    form = UserUpdateForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        user = models.User(id=user_id)
        new = user.update(username=form.username.data, role_id=form.role_id.data, password=form.password.data)
        return controller.render_json(data=new)

    return controller.render_json(code=-1, message=form.errors)


@bp_api.route('/user/<int:user_id>', methods=['DELETE'])
def user_remove(user_id):
    """
    删除用户: 删除用户信息, 删除用户组记录
    :param user_id:
    :return:
    """
    models.User(id=user_id).remove()
    models.Group().remove(user_id=user_id)
    return controller.render_json(message='')


@bp_api.route('/environment/', methods=['GET'])
def env_list():
    """
    环境列表

    :return:
    """
    page = int(request.args.get('page', 0))
    page = page - 1 if page else 0
    size = float(request.args.get('size', 10))
    kw = request.values.get('kw', '')

    env_model = models.Environment()
    env_list = env_model.list(page=page, size=size, kw=kw)
    return controller.render_json(data=env_list, count=13)


@bp_api.route('/environment/<int:env_id>', methods=['GET'])
def env_item(env_id):
    """
    获取某个用户组

    :param env_id:
    :return:
    """

    env_model = models.Environment(id=env_id)
    env_info = env_model.item()
    return controller.render_json(data=env_info)


@bp_api.route('/environment/', methods=['POST'])
def env_create():
    """
    添加用户组

    :return:
    """

    form = EnvironmentForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        env_new = models.Environment()
        ret = env_new.add(env_name=form.env_name.data)
        return controller.render_json(data=ret, message=env_new.to_json())
    else:
        return controller.render_json(code=-1, message=form.errors)


@bp_api.route('/environment/<int:env_id>', methods=['PUT'])
def env_update(env_id):
    """
    修改用户组

    :return:
    """

    form = EnvironmentForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        env = models.Environment(id=env_id)
        ret = env.update(env_name=form.env_name.data, status=form.status.data)
        return controller.render_json(data=env.to_json(), message=ret)
    else:
        return controller.render_json(code=-1, message=form.errors)



@bp_api.route('/environment/<int:env_id>', methods=['DELETE'])
def env_remove(env_id):
    env_model = models.Environment(id=env_id)
    env_model.remove(env_id)

    return controller.render_json(message='')
