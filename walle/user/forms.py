# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-19 15:50:07
    :author: wushuiyong@walle-web.io
"""
try:
    from flask_wtf import FlaskForm             # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm     # Fallback to Flask-WTF v0.12 or older
from flask_wtf import Form

from wtforms import BooleanField, HiddenField, PasswordField, SubmitField, StringField, TextField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired, Regexp
from walle.common.models import User

class UserForm(FlaskForm):
    pass

class RegistrationForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35),
                                        Regexp(r'^(.+)@(.+)\.(.+)', message='邮箱格式不正确')])
    password = PasswordField('Password', [validators.Length(min=6, max=35),
                                          Regexp(r'(?=\d{0,}[a-zA-Z])(?=[a-zA-Z]{0,}\d)[a-zA-Z0-9]{6,}', message='密码强度不足')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register')


class LoginForm(Form):

    email = TextField('Email Address', [validators.Length(min=6, max=35),
                                        Regexp(r'^(.+)@(.+)\.(.+)', message='邮箱格式不正确')])
    password = PasswordField('Password', [validators.Length(min=6, max=35),
                                          Regexp(r'(?=\d{0,}[a-zA-Z])(?=[a-zA-Z]{0,}\d)[a-zA-Z0-9]{6,}', message='密码强度不足')])

    def validate_email(self, field):
        pass
    # email = StringField('Email', validators=[validators.Required(), validators.Length(1, 64)]) #, validators.Email()
    # password = PasswordField('Password', validators=[validators.Required()])
