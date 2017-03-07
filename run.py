#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong@walle-web.io
# @Created Time : 二  2/14 08:47:47 2017
# @Description:

#!flask/bin/python
from walle import create_app

app = create_app()
app.run(debug = True)
