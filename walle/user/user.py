# -*- coding: utf-8 -*-
""" This file contains view functions for Flask-User forms.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details.
"""
import math
from flask import Blueprint, url_for, request

from flask import render_template
from walle.common import models
from walle.common.controller import Controller
from walle.user.forms import RegistrationForm

user_blue_print = Blueprint('user', __name__, static_folder='assets')

class User(Controller):
    taskModel = models.User()
    def list(self):
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 2))
        data = self.taskModel.list(page, size)
        count = self.taskModel.query.count()

        return self.render_json(data=data, count=int(math.ceil(count / size)))

    def one(self, uid=None, email=None):
        # task_id = int(request.args.get('task_id'))
        # data = self.taskModel.query.filter_by(id = task_id).one().to_json()
        #
        # return self.render_json(data=data)
        user_model = models.User()
        if uid:
            return user_model.query.filter_by(id=uid).first()
        elif email:
            return user_model.query.filter_by(email=email).first()
        # return self.render_json(data=item)

    def add(self, email, password):
        # 邮箱是否已经存在
        form = RegistrationForm(request.form)
        if (self.one(email=email)):
            return -1;
        elif(form.validate()):
            user_model = models.User(email=request.form.get('email'), password=request.form.get('password'))
            models.db.session.add(user_model)
            models.db.session.commit()
            return user_model.id
        return form.errors




user = User()


@user_blue_print.route('/')
@user_blue_print.route('/index')
def index():

    return render_template('user/signin.html')

@user_blue_print.route('/signup')
def signup():
    from walle.user.forms import RegistrationForm
    form = RegistrationForm(request.form)
    return render_template('user/signup.html', form=form)

@user_blue_print.route('/signin')
def signin():
    from walle.user.forms import RegistrationForm
    form = RegistrationForm(request.form)
    return render_template('user/signin.html', form=form)
