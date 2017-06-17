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


class ProjectAPI(Resource):
    def get(self, project_id=None):
        """
        fetch project list or one item
        /project/<int:project_id>

        :return:
        """
        return self.item(project_id) if project_id else self.list()

    def list(self):
        """
        fetch project list

        :return:
        """
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')

        project_model = models.Project()
        project_list, count = project_model.list(page=page, size=size, kw=kw)
        return Controller.list_json(list=project_list, count=count)

    def item(self, project_id):
        """
        获取某个用户组

        :param id:
        :return:
        """

        project_model = models.Project(id=project_id)
        project_info = project_model.item()
        if not project_info:
            return Controller.render_json(code=-1)
        return Controller.render_json(data=project_info)

    def post(self):
        """
        create a environment
        /environment/

        :return:
        """
        form = ProjectForm(request.form, csrf_enabled=False)
        # return Controller.render_json(code=-1, data = form.form2dict())
        if form.validate_on_submit():
            project_new = models.Project()
            data = form.form2dict()
            id = project_new.add(data)
            if not id:
                return Controller.render_json(code=-1)

            return Controller.render_json(data=project_new.item())
        else:
            return Controller.render_json(code=-1, message=form.errors)

    def put(self, project_id):
        """
        update environment
        /environment/<int:id>

        :return:
        """

        form = ProjectForm(request.form, csrf_enabled=False)
        form.set_id(project_id)
        if form.validate_on_submit():
            server = models.Project().get_by_id(project_id)
            data = form.form2dict()
            # a new type to update a model
            ret = server.update(data)
            return Controller.render_json(data=server.item())
        else:
            return Controller.render_json(code=-1, message=form.errors)

    def delete(self, project_id):
        """
        remove an environment
        /environment/<int:id>

        :return:
        """
        project_model = models.Project(id=project_id)
        project_model.remove(project_id)

        return Controller.render_json(message='')
