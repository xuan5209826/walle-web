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

from wtforms import TextField, IntegerField
from wtforms import validators


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
