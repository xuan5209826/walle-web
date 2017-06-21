# -*- coding: utf-8 -*-
"""Test Apis."""
from flask import json
import types
import urllib
import pytest
from utils import *
from walle.model.user import UserModel


@pytest.mark.usefixtures('db')
class TestApiPassport:
    """api role testing"""
    uri_prefix = '/api/passport'

    user_id = {}

    user_data = {
        'email': u'wushuiyong@walle-web.io',
        'password': u'wu123shuiyong',
    }

    user_name = u'wushuiyong@walle-web.io'

    def test_fetch(self):
        f=open('run.log', 'w')
        u = UserModel.get_by_id(1)
        f.write(str(u))

    def test_login(self, user, testapp, client, db):
        """create successful."""
        # 1.create another role
        query = {
            'page': 1,
            'size': 1,
            'kw': self.user_name
        }
        response = {
            'count': 1,
        }
        resp = client.get('/api/user/?%s' % (urllib.urlencode(query)))
        response_success(resp)
        compare_req_resp(response, resp)

        resp = client.post('%s/login' % (self.uri_prefix), data=self.user_data)

        response_success(resp)

        del self.user_data['password']
        compare_req_resp(self.user_data, resp)
