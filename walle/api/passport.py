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


class PassportAPI(Resource):
    action = ['login', 'logout']

    def post(self, method=None):
        """
        user login
        /passport/

        :return:
        """
        logging.error('======== logout ========')

        if method in self.action:
            self_method = getattr(self, method.lower(), None)
            return self_method()
        else:
            abort(404)


    def login(self):
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

    def logout(self):
        logging.error('======== logout ========')
        logout_user()
        return Controller.render_json()

