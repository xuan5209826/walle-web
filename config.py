# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-12 17:55:52
    :author: wushuiyong@walle-web.io
"""
import os

SRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI="mysql://walle:walle-web@localhost/walle_python"

#: cache settings
# find options on http://pythonhosted.org/Flask-Cache/
CACHE_TYPE = 'simple'

