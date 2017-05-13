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

from wtforms import BooleanField, HiddenField, PasswordField, SubmitField, StringField, TextField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired, Regexp
from walle.common.models import User, Role, Environment


class UserForm(FlaskForm):
    pass


class RegistrationForm(Form):
    email = TextField('Email Address', [validators.email()])
    password = PasswordField('Password', [validators.Length(min=6, max=35),
                                          Regexp(r'(?=\d{0,}[a-zA-Z])(?=[a-zA-Z]{0,}\d)[a-zA-Z0-9]{6,}',
                                                 message='密码强度不足')])

    role_id = TextField('Password', [validators.Length(min=1, max=10)])
    username = TextField('Password', [validators.Length(min=1, max=10)])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register')

    def validate_role_id(self, field):
        if not Role.query.filter_by(id=field.data).first():
            raise ValidationError('Email already register')


class UserUpdateForm(Form):
    password = PasswordField('Password', [validators.Length(min=0, max=35)])
    username = TextField('username', [validators.Length(min=1, max=10)])
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

    def validate_email(self, field):
        pass
        # email = StringField('Email', validators=[validators.Required(), validators.Length(1, 64)]) #, validators.Email()
        # password = PasswordField('Password', validators=[validators.Required()])


class RoleAdd(Form):
    name = TextField('Email Address', [validators.Length(min=6, max=35), validators.InputRequired()])
    # password = SelectField('Password', [validators.Length(min=6, max=35))


class GroupForm(Form):
    group_name = TextField('group_name', [validators.Length(min=1, max=10)])
    user_ids = TextField('user_ids', [validators.Length(min=1)])

    def validate_user_ids(self, field):
        user_ids = [int(uid) for uid in field.data.split(',')]
        if User.query.filter(User.id.in_(user_ids)).count() != len(user_ids):
            raise ValidationError('存在未记录的用户添加到用户组')


class EnvironmentForm(Form):
    env_name = TextField('env_name', [validators.Length(min=1, max=10)])
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



class TagCreateForm(Form):
    name = TextField('name', [validators.Length(min=1, max=10)])
    label = TextField('label', [validators.Length(min=1, max=30)])
