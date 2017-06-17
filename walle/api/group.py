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

class GroupAPI(Resource):
    def get(self, group_id=None):
        """
        用户组列表
        /group/

        :return:
        """
        return self.item(group_id) if group_id else self.list()

    def list(self):
        """
        用户组列表
        /group/

        :return:
        """
        page = int(request.args.get('page', 1))
        page = page if page else 1
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')
        filter = {'name': {'like': kw}} if kw else {}
        # f = open('run.log', 'w')
        # f.write(str(filter))

        group_model, count = models.Tag().query_paginate(page=page, limit=size, filter_name_dict=filter)
        groups = []
        for group_info in group_model:
            group_sub = models.Group.query \
                .filter_by(group_id=group_info.id) \
                .count()

            group_info = group_info.to_dict()
            group_info['users'] = group_sub
            group_info['group_id'] = group_info['id']
            group_info['group_name'] = group_info['name']
            groups.append(group_info)
        return Controller.list_json(list=groups, count=count)

    def item(self, group_id):
        """
        获取某个用户组
        /group/<int:group_id>

        :param group_id:
        :return:
        """
        ## sqlalchemy版本
        group_model = models.Group()
        group = group_model.item(group_id=group_id)
        if group:
            return Controller.render_json(data=group)
        return Controller.render_json(code=-1)

        ## mixin 版本
        group_model = models.Tag().get_by_id(group_id)
        if not group_model:
            return Controller.render_json(code=-1)

        f = open('run.log', 'w')
        # f.write(str(group_model) + '\n')
        user_ids = []
        for user_info in group_model.users:
            user_ids.append(user_info.user_id)
        group_info = group_model.to_dict()
        group_info['user_ids'] = user_ids
        group_info['users'] = len(user_ids)
        group_info['group_name'] = group_info['name']
        group_info['group_id'] = group_info['id']
        return Controller.render_json(data=group_info)

    def post(self):
        """
        create group
        /group/

        :return:
        """

        form = GroupForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            user_ids = [int(uid) for uid in form.user_ids.data.split(',')]

            group_new = models.Group()
            group_id = group_new.add(group_name=form.group_name.data, user_ids=user_ids)
            if not group_id:
                return Controller.render_json(code=-1)
            return Controller.render_json(data=group_new.item())
        else:
            return Controller.render_json(code=-1, message=form.errors)

    def put(self, group_id):
        """
        update group
        /group/<int:group_id>

        :return:
        """
        form = GroupForm(request.form, csrf_enabled=False)
        form.set_group_id(group_id)
        if form.validate_on_submit():
            user_ids = [int(uid) for uid in form.user_ids.data.split(',')]

            group_model = models.Group(group_id=group_id)
            group_model.update(group_id=group_id,
                               group_name=form.group_name.data,
                               user_ids=user_ids)
            return Controller.render_json(data=group_model.item())

        return Controller.render_json(code=-1, message=form.errors)

    def delete(self, group_id):
        """
        /group/<int:group_id>

        :return:
        """
        group_model = models.Group()
        tag_model = models.Tag()
        tag_model.remove(group_id)
        group_model.remove(group_id)

        return Controller.render_json(message='')

