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

