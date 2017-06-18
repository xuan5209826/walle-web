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

from walle.model.deploy import ProjectModel


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
        server = ProjectModel.query.filter_by(name=field.data).first()
        # 新建时,项目名不可与
        if server and server.id != self.id:
            raise ValidationError('该项目已重名')

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
