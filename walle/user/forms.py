# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-19 15:50:07
    :author: wushuiyong@walle-web.io
"""
try:
    from flask_wtf import FlaskForm  # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm  # Fallback to Flask-WTF v0.12 or older
from flask_wtf import Form

from wtforms import BooleanField, HiddenField, PasswordField, SubmitField, StringField, TextField, IntegerField, \
    TextAreaField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired, Regexp
from walle.common.models import User, Role, Environment, Tag, Server, Project


class UserForm(FlaskForm):
    pass


class RegistrationForm(Form):
    email = TextField('Email Address', [validators.email()])
    password = PasswordField('Password', [validators.Length(min=6, max=35),
                                          Regexp(r'(?=\d{0,}[a-zA-Z])(?=[a-zA-Z]{0,}\d)[a-zA-Z0-9]{6,}',
                                                 message='密码强度不足')])

    role_id = TextField('Password', [validators.Length(min=1, max=10)])
    username = TextField('Username', [validators.Length(min=1, max=50)])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register')

    def validate_role_id(self, field):
        if not Role.query.filter_by(id=field.data).first():
            raise ValidationError('Email already register')


class UserUpdateForm(Form):
    password = PasswordField('Password', [validators.Length(min=0, max=35)])
    username = TextField('username', [validators.Length(min=1, max=50)])
    role_id = TextField('role_id', [validators.Length(min=1, max=10)])

    def validate_password(self, field):
        if field.data and Regexp(r'(?=\d{0,}[a-zA-Z])(?=[a-zA-Z]{0,}\d)[a-zA-Z0-9]{6,}', message='密码强度不足'):
            raise ValidationError('密码强度不足')

    def validate_role_id(self, field):
        if not Role.query.filter_by(id=field.data).first():
            raise ValidationError('角色id不存在')


class LoginForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35),
                                        Regexp(r'^(.+)@(.+)\.(.+)', message='邮箱格式不正确')])
    password = PasswordField('Password', [validators.Length(min=6, max=35),
                                          Regexp(r'(?=\d{0,}[a-zA-Z])(?=[a-zA-Z]{0,}\d)[a-zA-Z0-9]{6,}',
                                                 message='密码强度不足')])


class RoleAdd(Form):
    name = TextField('Email Address', [validators.Length(min=6, max=35), validators.InputRequired()])
    # password = SelectField('Password', [validators.Length(min=6, max=35))


class GroupForm(Form):
    group_name = TextField('group_name', [validators.Length(min=1, max=100)])
    user_ids = TextField('user_ids', [validators.Length(min=1)])
    group_id = None

    def set_group_id(self, group_id):
        self.group_id = group_id

    def validate_user_ids(self, field):
        user_ids = [int(uid) for uid in field.data.split(',')]
        if User.query.filter(User.id.in_(user_ids)).count() != len(user_ids):
            raise ValidationError('存在未记录的用户添加到用户组')

    def validate_group_name(self, field):
        env = Tag.query.filter_by(name=field.data).filter_by(label='user_group').first()
        # 新建时,环境名不可与
        if env and env.id != self.group_id:
            raise ValidationError('该用户组已经配置过')


class EnvironmentForm(Form):
    env_name = TextField('env_name', [validators.Length(min=1, max=100)])
    status = TextField('status', [validators.Length(min=0, max=10)])
    env_id = None

    def set_env_id(self, env_id):
        self.env_id = env_id

    def validate_env_name(self, field):
        env = Environment.query.filter_by(name=field.data).first()
        # 新建时,环境名不可与
        if env and env.id != self.env_id:
            raise ValidationError('该环境已经配置过')

    def validate_status(self, field):
        if field.data and int(field.data) not in [1, 2]:
            raise ValidationError('非法的状态')


class ServerForm(Form):
    name = TextField('name', [validators.Length(min=1, max=100)])
    host = TextField('host', [validators.Length(min=1, max=100)])
    id = None

    def set_id(self, id):
        self.id = id

    def validate_name(self, field):
        server = Server.query.filter_by(name=field.data).first()
        # 新建时,环境名不可与
        if server and server.id != self.id:
            raise ValidationError('该Server已重名')


class TagCreateForm(Form):
    name = TextField('name', [validators.Length(min=1, max=10)])
    label = TextField('label', [validators.Length(min=1, max=30)])


class ProjectForm(Form):
    name = TextField('name', [validators.Length(min=1, max=100)])
    environment_id = TextField('environment_id', [validators.Length(min=1, max=10)])
    excludes = TextField('excludes', [validators.Length(min=1)])
    server_ids = TextField('server_ids', [validators.Length(min=1)])
    keep_version_num = TextField('keep_version_num', [validators.Length(min=1, max=2)])

    target_user = TextField('target_user', [validators.Length(min=1, max=50)])
    target_root = TextField('target_root', [validators.Length(min=1, max=200)])
    target_library = TextField('target_library', [validators.Length(min=1, max=200)])

    task_vars = TextField('task_vars', [validators.Length(min=1)])
    prev_deploy = TextField('prev_deploy', [validators.Length(min=1)])
    post_deploy = TextField('post_deploy', [validators.Length(min=1)])
    prev_release = TextField('prev_release', [validators.Length(min=1)])
    post_release = TextField('post_release', [validators.Length(min=1)])

    repo_url = TextField('repo_url', [validators.Length(min=1, max=200)])
    repo_username = TextField('repo_username', [validators.Length(min=0, max=50)])
    repo_password = TextField('repo_password', [validators.Length(min=0, max=50)])
    repo_mode = TextField('repo_mode', [validators.Length(min=1, max=50)])

    id = None

    def set_id(self, id):
        self.id = id

    def validate_name(self, field):
        server = Project.query.filter_by(name=field.data).first()
        # 新建时,项目名不可与
        if server and server.id != self.id:
            raise ValidationError('该Server已重名')

    def form2dict(self):
        return {
            'name': self.name.data if self.name.data else '',
            # todo g.uid
            'user_id': 1,
            'environment_id': self.environment_id.data if self.environment_id.data else '',
            'excludes': self.excludes.data if self.excludes.data else '',
            'server_ids': self.server_ids.data if self.server_ids.data else '',
            'keep_version_num': self.keep_version_num.data if self.keep_version_num.data else '',

            'target_user': self.target_user.data if self.target_user.data else '',
            'target_root': self.target_root.data if self.target_root.data else '',
            'target_library': self.target_library.data if self.target_library.data else '',

            'task_vars': self.task_vars.data if self.task_vars.data else '',
            'prev_deploy': self.prev_deploy.data if self.prev_deploy.data else '',
            'post_deploy': self.post_deploy.data if self.post_deploy.data else '',
            'prev_release': self.prev_release.data if self.prev_release.data else '',
            'post_release': self.post_release.data if self.post_release.data else '',

            'repo_url': self.repo_url.data if self.repo_url.data else '',
            'repo_username': self.repo_username.data if self.repo_username.data else '',
            'repo_password': self.repo_password.data if self.repo_password.data else '',
            'repo_mode': self.repo_mode.data if self.repo_mode.data else '',
        }


class TaskForm(Form):
    name = TextField('name', [validators.Length(min=1)])
    project_id = IntegerField('project_id', [validators.NumberRange(min=1)])
    servers = TextField('servers', [validators.Length(min=1)])
    commit_id = TextField('commit_id', [validators.Length(min=1)])
    branch = TextField('branch', [validators.Length(min=1)])
    file_transmission_mode = IntegerField('file_transmission_mode', [validators.NumberRange(min=0)])
    file_list = TextField('file_list', [validators.Length(min=1)])

    id = None

    def set_id(self, id):
        self.id = id

    def form2dict(self):
        return {
            'name': self.name.data if self.name.data else '',
            # todo
            'user_id': 1,
            'project_id': self.project_id.data if self.project_id.data else '',
            # todo default value
            'action': 0,
            'status': 0,
            'link_id': '',
            'ex_link_id': '',
            'servers': self.servers.data if self.servers.data else '',
            'commit_id': self.commit_id.data if self.commit_id.data else '',
            'branch': self.branch.data if self.branch.data else '',
            'file_transmission_mode': self.file_transmission_mode.data if self.file_transmission_mode.data else 0,
            'file_list': self.file_list.data if self.file_list.data else '',
            'enable_rollback': 1,

        }
