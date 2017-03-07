# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-02-16 08:46:33
    :author: wushuiyong@walle-web.io
"""

from flask import render_template
from flask import Blueprint, url_for

deploy = Blueprint('deploy', __name__, static_folder='assets')


@deploy.route('/')
@deploy.route('/index')
def index():
    user = { 'nickname': 'Miguel' + url_for('static', filename='css/ace.min.css') } # fake user
    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("deploy/blank.html",
        title = 'Home',
        user = user,
        posts = posts)

@deploy.route('/test')
def testss():
    user = { 'nickname': 'test' + url_for('static', filename='css/ace.min.css') } # fake user
    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("deploy/blank.html",
        title = 'Home',
        user = user,
        posts = posts)