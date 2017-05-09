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

@bp_api.route('/role/', methods=['GET', 'POST'])
@bp_api.route('/role/list', methods=['GET', 'POST'])
def role_list():
    page = int(request.args.get('page', 0))
    page = page - 1 if page else 0
    size = float(request.args.get('size', 2))
    kw = request.values.get('kw', '')

    role_model = models.Role()
    role_list = role_model.list(page=page, size=size, kw=kw)
    return controller.render_json(data=role_list, count=13)


@bp_api.route('/role/item', methods=['GET', 'POST'])
def role_item():
    role_id = request.args.get('role_id', 0)
    role_model = models.Role()
    if role_id:
        role_info = role_model.item(role_id)
        return controller.render_json(data=role_info)

    return controller.render_json()


@bp_api.route('/role/update', methods=['GET', 'POST'])
def role_update():
    role_id = request.args.get('role_id', 0)
    role_model = models.Role()
    if role_id:
        role_info = role_model.item(role_id)
        return controller.render_json(data=role_info)

    return controller.render_json()

@bp_api.route('/role/remove', methods=['GET', 'POST'])
def role_remove():
    role_id = request.args.get('role_id', 0)
    role_model = models.Role()
    if role_id:
        return role_model.remove(role_id)

    return controller.render_json()

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



@bp_api.route('/group/', methods=['GET', 'POST'])
@bp_api.route('/group/list', methods=['GET', 'POST'])
def group_list():
    page = int(request.args.get('page', 0))
    page = page - 1 if page else 0
    size = float(request.args.get('size', 10))
    kw = request.values.get('kw', '')

    group_model = models.Group()
    group_list = group_model.list(page=page, size=size, kw=kw)
    return controller.render_json(data=group_list, count=13)


@bp_api.route('/group/item', methods=['GET', 'POST'])
def group_item():
    group_id = request.args.get('group_id', 0)
    group_model = models.Group()
    if group_id:
        group_info = group_model.item(group_id)
        return controller.render_json(data=group_info)

    return controller.render_json()


@bp_api.route('/group/update', methods=['GET', 'POST'])
def group_update():
    group_id = request.args.get('group_id', 0)
    group_name = request.args.get('group_name', None)
    group_model = models.Group()
    if group_id and group_name:
        group_info = group_model.update(group_id, group_name)
        return controller.render_json(data=group_info)
    elif group_name:
        ret = group_model.add(group_name)
        return controller.render_json(data=ret)

    return controller.render_json()

@bp_api.route('/group/remove', methods=['GET', 'POST'])
def group_remove():
    group_id = request.args.get('group_id', 0)
    group_model = models.Group()
    if group_id:
        return group_model.remove(group_id)

    return controller.render_json()
