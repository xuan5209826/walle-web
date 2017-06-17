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


class RoleAPI(Resource):
    """
    角色没有上下级, 一个角色的用户可以看到
    1.超管
    2.研发总监, 产品总监
    3.FE Leader, QA Leader, RD Leader
    4.FE 1, FE 2, FE 3

    场景：
    1.项目管理:下级角色建立的项目,上级是否可见可写
    2.上线单管理：下级角色提交的上线单，上级是否可以操作
    """

    def get(self, role_id=None):
        """
        fetch role list or one role

        :return:
        """
        return self.item(role_id) if role_id else self.list()

    def list(self):
        """
        fetch role list
        /role/

        :return:
        """
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')

        role_model = models.Role()
        role_list, count = role_model.list(page=page, size=size, kw=kw)
        return Controller.list_json(list=role_list, count=count)

    def item(self, role_id):
        """
        fetch one role
        /role/<int:role_id>

        :param role_id:
        :return:
        """
        role_model = models.Role(id=role_id)
        role_info = role_model.item()
        if not role_info:
            return Controller.render_json(code=-1)
        return Controller.render_json(data=role_info)

    def post(self):
        """
        新增角色
        /role/

        :return:
        """
        role_name = request.form.get('role_name', None)
        role_permissions_ids = request.form.get('access_ids', '')
        role_model = models.Role()
        role_id = role_model.add(name=role_name, access_ids=role_permissions_ids)

        if not role_id:
            Controller.render_json(code=-1)
        return Controller.render_json(data=role_model.item())

    def put(self, role_id):
        """
        修改角色
        /role/<int:role_id>

        :param role_id:
        :return:
        """
        role_name = request.form.get('role_name', None)
        role_access_ids = request.form.get('access_ids', '')

        if not role_name:
            return Controller.render_json(code=-1, message='role_name can not be empty')

        role_model = models.Role(id=role_id)
        ret = role_model.update(name=role_name, access_ids=role_access_ids)
        return Controller.render_json(data=role_model.item())

    def delete(self, role_id):
        """
        删除一个角色
        /role/<int:role_id>

        :return:
        """
        role_model = models.Role(id=role_id)
        ret = role_model.remove()

        return Controller.render_json(code=0)

