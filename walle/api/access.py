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
from walle.api.base import SecurityResource

import os
from flask.ext.login import LoginManager, login_required
from walle.extensions import login_manager
import logging

class AccessAPI(SecurityResource):
    controller = 'access'

    """
    权限是以resource + method作为一个access

    """
    # @login_required
    def get(self, access_id=None):
        # super(AccessAPI, self).get()
        """
        fetch access list or one access

        :return:
        """
        return self.item(access_id) if access_id else self.list()

    def list(self):
        """
        fetch access list
        /access/

        :return:
        """

        access_model = models.Access()
        access_list = access_model.list()
        return Controller.render_json(data=access_list)

    def item(self, access_id):
        """
        fetch one access
        /access/<int:access_id>

        :param access_id:
        :return:
        """
        access_model = models.Role(id=access_id)
        access_info = access_model.item()
        if not access_info:
            return Controller.render_json(code=-1)
        return Controller.render_json(data=access_info)

    def post(self):
        """
        新增角色
        /access/

        :return:
        """
        access_name = request.form.get('access_name', None)
        access_permissions_ids = request.form.get('access_ids', '')
        access_model = models.Role()
        access_id = access_model.add(name=access_name, access_ids=access_permissions_ids)

        if not access_id:
            Controller.render_json(code=-1)
        return Controller.render_json(data=access_model.item())

    def put(self, access_id):
        """
        修改角色
        /access/<int:access_id>

        :param access_id:
        :return:
        """
        access_name = request.form.get('access_name', None)
        access_ids = request.form.get('access_ids', '')

        if not access_name:
            return Controller.render_json(code=-1, message='access_name can not be empty')

        access_model = models.Role(id=access_id)
        ret = access_model.update(name=access_name, access_ids=access_ids)
        return Controller.render_json(data=access_model.item())

    def delete(self, access_id):
        """
        删除一个角色
        /access/<int:access_id>

        :return:
        """
        access_model = models.Role(id=access_id)
        ret = access_model.remove()

        return Controller.render_json(code=0)
