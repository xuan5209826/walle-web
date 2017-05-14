# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-25 11:15:01
    :author: wushuiyong@walle-web.io
"""


from walle.common import models
from walle.common.controller import Controller
from walle.user.forms import UserUpdateForm, GroupForm, EnvironmentForm
from flask.ext.login import current_user
from flask.ext.login import login_user
from walle.user.forms import RegistrationForm, LoginForm
from flask import request
from flask.ext.restful import Resource

from walle.common.models import db
from werkzeug.security import generate_password_hash


class RoleAPI(Resource):
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
        return Controller.render_json(data=role_info)

    def post(self):
        """
        新增角色
        /role/

        :return:
        """
        role_name = request.form.get('role_name', None)
        role_permissions_ids = request.form.get('permission_ids', '')
        role_model = models.Role()
        role_id = role_model.add(name=role_name, permission_ids=role_permissions_ids)

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
        role_permission_ids = request.form.get('permission_ids', '')

        if not role_name:
            return Controller.render_json(code=-1, message='role_name can not be empty')

        role_model = models.Role(id=role_id)
        ret = role_model.update(name=role_name, permission_ids=role_permission_ids)
        return Controller.render_json(code=ret, data=role_model.item())

    def delete(self, role_id):
        """
        删除一个角色
        /role/<int:role_id>

        :return:
        """
        role_model = models.Role(id=role_id)
        ret = role_model.remove()

        return Controller.render_json(code=0)


class PassportAPI(Resource):
    def post(self):
        """
        user login
        /passport/

        :return:
        """
        form = LoginForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            user = models.User.query.filter_by(email=form.email.data).first()

            if user is not None and user.verify_password(form.password.data):
                login_user(user)
                return Controller.render_json(data=current_user.to_json())

        return Controller.render_json(code=-1, data=form.errors)


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
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')

        group_model = models.Group()
        group_list, count = group_model.list(page=page, size=size, kw=kw)

        groups = []
        for group_item in group_list:
            group_item['users'] = len(group_item['users'])
            del group_item['label'], group_item['updated_at']
            groups.append(group_item)

        return Controller.list_json(list=group_list, count=count)

    def item(self, group_id):
        """
        获取某个用户组
        /group/<int:group_id>

        :param group_id:
        :return:
        """

        group_model = models.Group(group_id=group_id)
        group_info = group_model.item()

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
            return Controller.render_json(data=user.item())
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
