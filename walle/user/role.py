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
from walle.user.forms import RoleAdd

# role_blue_print = Blueprint('role', __name__, static_folder='assets')
role_blue_print = Blueprint('role', __name__)

class Role(Controller):
    roleModel = models.Role()


    def list(self):
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 2))
        data = self.roleModel.list(page, size)
        count = self.roleModel.query.count()

        return self.render_json(data=data, count=int(math.ceil(count / size)))

    def one(self, uid=None, email=None):
        role_model = models.User()
        if uid:
            return role_model.query.filter_by(id=uid).first()
        elif email:
            return role_model.query.filter_by(email=email).first()

    def add(self, email, password):
        # 邮箱是否已经存在
        form = RegistrationForm(request.form)
        if (self.one(email=email)):
            return -1;
        elif(form.validate()):
            role_model = models.User(email=request.form.get('email'), password=request.form.get('password'))
            models.db.session.add(role_model)
            models.db.session.commit()
            return role_model.id
        return form.errors



@role_blue_print.route('/')
@role_blue_print.route('/index')
def index():

    return render_template('role/list.html')

@role_blue_print.route('/add')
def add():
    form = RoleAdd(request.form)
    return render_template('role/add.html', form=form)

@role_blue_print.route('/update')
def update():
    from walle.user.forms import RegistrationForm
    form = RegistrationForm(request.form)
    return render_template('user/info.html', form=form)

@role_blue_print.route('/remove')
def remove():
    from walle.user.forms import RegistrationForm
    form = RegistrationForm(request.form)
    return render_template('user/remove.html', form=form)


