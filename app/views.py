#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong@walle-web.io
# @Created Time : 二  2/14 08:46:57 2017
# @Description:

from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
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
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)