# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-02-16 08:46:33
    :author: wushuiyong@walle-web.io
"""
import math
from flask import Blueprint, url_for, request
from flask import render_template

from walle.common import models
from walle.common.controller import Controller

deploy = Blueprint('deploy', __name__, static_folder='assets')

class Deploy(Controller):
    taskModel = models.Task()
    def list(self):
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 2))
        data = self.taskModel.list(page, size)
        count = self.taskModel.query.count()

        return self.render_json(data=data, count=int(math.ceil(count / size)))

    def one(self):
        # task_id = int(request.args.get('task_id'))
        # data = self.taskModel.query.filter_by(id = task_id).one().to_json()
        #
        # return self.render_json(data=data)
        taskModel = models.Task(task_id=1)
        return self.render_json(data=taskModel.one())





deployer = Deploy()


@deploy.route('/')
@deploy.route('/index')
def index():

    return render_template('deploy/index.html')

@deploy.route('/list')
def list():
    return deployer.list()

@deploy.route('/task')
def task():
    return deployer.one()


@deploy.route('/start')
def start():
    return render_template("deploy/start.html",)

@deploy.route('/mail')
def mail():
    from walle.common import emails
    user = models.User.query.filter_by(id=1).one()
    d = Deploy()
    # return d.render_json(data=user.username)
    # return d.render_json(data=user.username)

    ret = emails.public_send_registered_email(user)

    return d.render_json(data=ret)

@deploy.route('/confirm_mail')
def confirm_mail():
    from walle.common import emails
    user = models.User.query.filter_by(id=1).one()
    d = Deploy()
    # return d.render_json(data=user.username)

    emails.public_send_registered_email(user)