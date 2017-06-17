# -*- coding: utf-8 -*-
"""

    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-25 11:15:01
    :author: wushuiyong@walle-web.io
"""

from walle.model import models
from walle.common.controller import Controller
from walle.form.forms import UserUpdateForm, GroupForm, EnvironmentForm, ServerForm, TaskForm, RegistrationForm, LoginForm, ProjectForm
from flask_login import current_user
from flask_login import login_user, logout_user
from flask import request, abort
from flask_restful import Resource

from walle.service.rbac.access import Access

from walle.model.models import db
from werkzeug.security import generate_password_hash
from datetime import datetime
import time
from werkzeug.utils import secure_filename
import os
from flask.ext.login import LoginManager, login_required
from walle.extensions import login_manager
import logging


class UserAPI(Resource):
    def get(self, user_id=None):
        """
        fetch user list or one user
        /user/<int:user_id>

        :return:
        """
        return self.item(user_id) if user_id else self.list()

    def list(self):
        """
        fetch user list or one user

        :return:
        """
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')

        user_model = models.User()
        user_list, count = user_model.list(page=page, size=size, kw=kw)
        return Controller.list_json(list=user_list, count=count)

    def item(self, user_id):
        """
        获取某个用户

        :param user_id:
        :return:
        """

        user_info = models.User(id=user_id).item()
        if not user_info:
            return Controller.render_json(code=-1)
        return Controller.render_json(data=user_info)

    def post(self):
        """
        create user
        /user/

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
            return Controller.render_json(data=user.item(user_id=user.id))
        return Controller.render_json(code=-1, message=form.errors)

    def put(self, user_id):
        """
        edit user
        /user/<int:user_id>

        :return:
        """
        form = UserUpdateForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            user = models.User(id=user_id)
            user.update(username=form.username.data, role_id=form.role_id.data, password=form.password.data)
            return Controller.render_json(data=user.item())

        return Controller.render_json(code=-1, message=form.errors)

    def delete(self, user_id):
        """
        remove a user with his group relation
        /user/<int:user_id>

        :param user_id:
        :return:
        """
        models.User(id=user_id).remove()
        models.Group().remove(user_id=user_id)
        return Controller.render_json(message='')
