# -*- coding: utf-8 -*-
""" This file contains view functions for Flask-User forms.

    :copyright: (c) 2013 by Ling Thio
    :author: Ling Thio (ling.thio@gmail.com)
    :license: Simplified BSD License, see LICENSE.txt for more details."""
import math
from flask import Blueprint, url_for, request, redirect
from flask import render_template
from flask.ext.login import login_user
from walle.common import models
from walle.common.models import db
from walle.common.controller import Controller
from walle.user.user import User
from walle.user.forms import RegistrationForm, LoginForm
from werkzeug.security import check_password_hash,generate_password_hash
from flask.ext.login import current_user
# from walle import login_manager

passport_blue_print = Blueprint('passport', __name__, static_folder='assets')

controler = Controller()
@passport_blue_print.route('/email_exists', methods=['GET', 'POST'])
def email_exists():
    user = User()
    item = user.one(email=request.args.get('email'))
    code = -1 if item else 0
    return controler.render_json(code=code, data=item.to_json())


@passport_blue_print.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        user = models.User(email=form.email.data,
                    username=form.email.data,
                    password=password)
        db.session.add(user)
        db.session.commit()
        return controler.render_json(data={'user_id':user.id, 'oldpwd': password,'password':generate_password_hash(form.password.data)})
        return redirect(url_for('passport.signin'))
    return controler.render_json(code=-1)

    user = User()
    done = user.add(email=request.form.get('email'), password=request.form.get('password'))
    return controler.render_json(data=done)
    code = -1 if done else 0
    return controler.render_json(code=code, data=done)

@passport_blue_print.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return controler.render_json(data={'user_info': current_user.to_json()})

    return controler.render_json(code=-1, data=form.errors)

@passport_blue_print.route('/info', methods=['GET', 'POST'])
def info():
    return controler.render_json(data={'user_info':current_user.to_json()})


