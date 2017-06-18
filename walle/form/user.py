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
from wtforms import PasswordField, TextField
from wtforms import validators, ValidationError
from wtforms.validators import Regexp

from walle.model.user import RoleModel
from walle.model.user import UserModel


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
        if UserModel.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register')

    def validate_role_id(self, field):
        if not RoleModel.query.filter_by(id=field.data).first():
            raise ValidationError('Email already register')


class UserUpdateForm(Form):
    password = PasswordField('Password', [validators.Length(min=0, max=35)])
    username = TextField('username', [validators.Length(min=1, max=50)])
    role_id = TextField('role_id', [validators.Length(min=1, max=10)])

    def validate_password(self, field):
        if field.data and Regexp(r'(?=\d{0,}[a-zA-Z])(?=[a-zA-Z]{0,}\d)[a-zA-Z0-9]{6,}', message='密码强度不足'):
            raise ValidationError('密码强度不足')

    def validate_role_id(self, field):
        if not RoleModel.query.filter_by(id=field.data).first():
            raise ValidationError('角色id不存在')


class LoginForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35),
                                        Regexp(r'^(.+)@(.+)\.(.+)', message='邮箱格式不正确')])
    password = PasswordField('Password', [validators.Length(min=6, max=35),
                                          Regexp(r'(?=\d{0,}[a-zA-Z])(?=[a-zA-Z]{0,}\d)[a-zA-Z0-9]{6,}',
                                                 message='密码强度不足')])
