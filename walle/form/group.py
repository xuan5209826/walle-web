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
from wtforms import TextField
from wtforms import validators, ValidationError

from walle.model.user import UserModel
from walle.model.tag import TagModel


class GroupForm(Form):
    group_name = TextField('group_name', [validators.Length(min=1, max=100)])
    user_ids = TextField('user_ids', [validators.Length(min=1)])
    group_id = None

    def set_group_id(self, group_id):
        self.group_id = group_id

    def validate_user_ids(self, field):
        user_ids = [int(uid) for uid in field.data.split(',')]
        if UserModel.query.filter(UserModel.id.in_(user_ids)).count() != len(user_ids):
            raise ValidationError('存在未记录的用户添加到用户组')

    def validate_group_name(self, field):
        env = TagModel.query.filter_by(name=field.data).filter_by(label='user_group').first()
        # 新建时,环境名不可与
        if env and env.id != self.group_id:
            raise ValidationError('该用户组已经配置过')
