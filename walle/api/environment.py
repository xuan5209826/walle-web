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


class EnvironmentAPI(Resource):
    def get(self, env_id=None):
        """
        fetch environment list or one item
        /environment/<int:env_id>

        :return:
        """
        return self.item(env_id) if env_id else self.list()

    def list(self):
        """
        fetch environment list

        :return:
        """
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')

        env_model = models.Environment()
        env_list, count = env_model.list(page=page, size=size, kw=kw)
        return Controller.list_json(list=env_list, count=count)

    def item(self, env_id):
        """
        获取某个用户组

        :param env_id:
        :return:
        """

        env_model = models.Environment(id=env_id)
        env_info = env_model.item()
        if not env_info:
            return Controller.render_json(code=-1)
        return Controller.render_json(data=env_info)

    def post(self):
        """
        create a environment
        /environment/

        :return:
        """

        form = EnvironmentForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            env_new = models.Environment()
            env_id = env_new.add(env_name=form.env_name.data)
            if not env_id:
                return Controller.render_json(code=-1)
            return Controller.render_json(data=env_new.item())
        else:
            return Controller.render_json(code=-1, message=form.errors)

    def put(self, env_id):
        """
        update environment
        /environment/<int:env_id>

        :return:
        """

        form = EnvironmentForm(request.form, csrf_enabled=False)
        form.set_env_id(env_id)
        if form.validate_on_submit():
            env = models.Environment(id=env_id)
            ret = env.update(env_name=form.env_name.data, status=form.status.data)
            return Controller.render_json(data=env.item())
        else:
            return Controller.render_json(code=-1, message=form.errors)

    def delete(self, env_id):
        """
        remove an environment
        /environment/<int:env_id>

        :return:
        """
        env_model = models.Environment(id=env_id)
        env_model.remove(env_id)

        return Controller.render_json(message='')
