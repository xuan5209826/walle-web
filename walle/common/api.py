# -*- coding: utf-8 -*-
"""

    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-25 11:15:01
    :author: wushuiyong@walle-web.io
"""

from walle.common import models
from walle.common.controller import Controller
from walle.user.forms import UserUpdateForm, GroupForm, EnvironmentForm, ServerForm, TaskForm
from flask_login import current_user
from flask_login import login_user
from walle.user.forms import RegistrationForm, LoginForm, ProjectForm
from flask import request
from flask_restful import Resource

from walle.rbac.access import Access

from walle.common.models import db
from werkzeug.security import generate_password_hash
from datetime import datetime
import time
from werkzeug.utils import secure_filename
import os


class Base(Resource):
    def get(self):
        """
        fetch role list or one role

        :return:
        """
        return 'walle-web 2.0'


class PublicAPI(Resource):
    def get(self, method):
        """
        fetch role list or one role

        :return:
        """
        if method == 'menu':
            return self.menu()

    def post(self, method):
        """
        fetch role list or one role

        :return:
        """
        if method == 'avater':
            return self.avater()

    def menu(self):
        user = models.User(id=1).item()
        menu = Access().get_menu()
        data = {
            'user': user,
            'menu': menu,
        }
        return Controller.render_json(data=data)

    def avater(self):
        UPLOAD_FOLDER = 'fe/public/avater'
        f = request.files['avater']
        fname = secure_filename(f.filename)
        # todo rename to uid relation
        fname = secure_filename(f.filename)
        ret = f.save(os.path.join(UPLOAD_FOLDER, fname))

        return Controller.render_json(data={
            'avarter': fname,
        })


class AccessAPI(Resource):
    """
    权限是以resource + method作为一个access

    """

    def get(self, access_id=None):
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


class PassportAPI(Resource):
    def post(self):
        """
        user login
        /passport/

        :return:
        """
        f = open('run.log', 'w')
        form = LoginForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            # f.write('\n' + form.email.data + '\n')
            user = models.User.query.filter_by(email=form.email.data).first()
            # f.write('\n' + str(user) + '\n')
            # f.write('\n' + str(user) + '\n')

            if user is not None and user.verify_password(form.password.data):
                login_user(user)
                return Controller.render_json(data=current_user.to_json())

        f.write('\nvalidata fail\n')

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


class TaskAPI(Resource):
    def get(self, task_id=None):
        """
        fetch user list or one user
        /task/<int:user_id>

        :return:
        """
        return self.item(task_id) if task_id else self.list()

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

    def item(self, task_id):
        """
        获取某个用户

        :param task_id:
        :return:
        """

        user_info = models.User(id=task_id).item()
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
            return Controller.render_json(data=user.item(task_id=user.id))
        return Controller.render_json(code=-1, message=form.errors)

    def put(self, task_id):
        """
        edit user
        /user/<int:task_id>

        :return:
        """
        form = UserUpdateForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            user = models.User(id=task_id)
            user.update(username=form.username.data, role_id=form.role_id.data, password=form.password.data)
            return Controller.render_json(data=user.item())

        return Controller.render_json(code=-1, message=form.errors)

    def delete(self, task_id):
        """
        remove a user with his group relation
        /user/<int:task_id>

        :param task_id:
        :return:
        """
        models.User(id=task_id).remove()
        models.Group().remove(task_id=task_id)
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


class ServerAPI(Resource):
    def get(self, id=None):
        """
        fetch environment list or one item
        /environment/<int:env_id>

        :return:
        """
        return self.item(id) if id else self.list()

    def list(self):
        """
        fetch environment list

        :return:
        """
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')

        server_model = models.Server()
        server_list, count = server_model.list(page=page, size=size, kw=kw)
        return Controller.list_json(list=server_list, count=count)

    def item(self, id):
        """
        获取某个用户组

        :param id:
        :return:
        """

        server_model = models.Server(id=id)
        server_info = server_model.item()
        if not server_info:
            return Controller.render_json(code=-1)
        return Controller.render_json(data=server_info)

    def post(self):
        """
        create a environment
        /environment/

        :return:
        """

        form = ServerForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            server_new = models.Server()
            id = server_new.add(name=form.name.data, host=form.host.data)
            if not id:
                return Controller.render_json(code=-1)

            return Controller.render_json(data=server_new.item())
        else:
            return Controller.render_json(code=-1, message=form.errors)

    def put(self, id):
        """
        update environment
        /environment/<int:id>

        :return:
        """

        form = ServerForm(request.form, csrf_enabled=False)
        form.set_id(id)
        if form.validate_on_submit():
            server = models.Server(id=id)
            ret = server.update(name=form.name.data, host=form.host.data)
            return Controller.render_json(data=server.item())
        else:
            return Controller.render_json(code=-1, message=form.errors)

    def delete(self, id):
        """
        remove an environment
        /environment/<int:id>

        :return:
        """
        server_model = models.Server(id=id)
        server_model.remove(id)

        return Controller.render_json(message='')


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


class TaskAPI(Resource):
    def get(self, task_id=None):
        """
        fetch project list or one item
        /project/<int:project_id>

        :return:
        """
        return self.item(task_id) if task_id else self.list()

    def list(self):
        """
        fetch project list

        :return:
        """
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')

        task_model = models.Task()
        task_list, count = task_model.list(page=page, size=size, kw=kw)
        return Controller.list_json(list=task_list, count=count)

    def item(self, task_id):
        """
        获取某个用户组

        :param id:
        :return:
        """

        task_model = models.Task(id=task_id)
        task_info = task_model.item()
        if not task_info:
            return Controller.render_json(code=-1)
        return Controller.render_json(data=task_info)

    def post(self):
        """
        create a environment
        /environment/

        :return:
        """
        form = TaskForm(request.form, csrf_enabled=False)
        # return Controller.render_json(code=-1, data = form.form2dict())
        if form.validate_on_submit():
            task_new = models.Task()
            data = form.form2dict()
            id = task_new.add(data)
            if not id:
                return Controller.render_json(code=-1)

            return Controller.render_json(data=task_new.item())
        else:
            return Controller.render_json(code=-1, message=form.errors)

    def put(self, task_id):
        """
        update environment
        /environment/<int:id>

        :return:
        """

        form = TaskForm(request.form, csrf_enabled=False)
        f = open('run.log', 'w')
        form.set_id(task_id)
        if form.validate_on_submit():
            task = models.Task().get_by_id(task_id)
            data = form.form2dict()
            f.write('\n====form2dict===\n' + str(data))
            # a new type to update a model
            ret = task.update(data)
            return Controller.render_json(data=task.item())
        else:
            return Controller.render_json(code=-1, message=form.errors)

    def delete(self, task_id):
        """
        remove an environment
        /environment/<int:id>

        :return:
        """
        task_model = models.Task(id=task_id)
        task_model.remove(task_id)

        return Controller.render_json(message='')


class FooAPI(Resource):
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
        page = page + 1 if page else 1
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')
        filter = {'username': {'like': request.args.get('username')}} if kw else {}
        foo, count = models.Foo().query_paginate(page=page, limit=size, filter_name_dict=filter)
        # ret = foo.update(username=request.form.get('username'), email=request.form.get('email'))
        return Controller.list_json(list=[i.to_dict() for i in foo], count=count)

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
        foo = models.Foo().get_by_id(env_id)
        # ret = foo.update(username=request.form.get('username'), email=request.form.get('email'))
        return Controller.render_json(data=foo.to_dict())

    def post(self):
        """
        create a environment
        /environment/

        :return:
        """
        foo = models.Foo()
        ret = foo.create(username=request.form.get('username'), email=request.form.get('email'))
        return Controller.render_json(data=ret.to_dict())

    def put(self, env_id):
        """
        update environment
        /environment/<int:env_id>

        :return:
        """

        foo = models.Foo(id=env_id)
        # ret = foo.update(username=request.form.get('username'), email=request.form.get('email'))
        return Controller.render_json(data=foo.to_dict())

    def delete(self, env_id):
        """
        remove an environment
        /environment/<int:env_id>

        :return:
        """
        env_model = models.Environment(id=env_id)
        env_model.remove(env_id)

        return Controller.render_json(message='')
