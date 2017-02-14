#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong@walle-web.io
# @Created Time : 二  2/14 08:46:33 2017
# @Description:
from flask import Flask

app = Flask(__name__)
from app import views
