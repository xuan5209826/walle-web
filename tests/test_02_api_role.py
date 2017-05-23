# -*- coding: utf-8 -*-
"""Test Apis."""
from flask import json
import types
import urllib
import pytest
from utils import *


@pytest.mark.usefixtures('db')
class TestApiRole:
    """api role testing"""
    uri_prefix = '/api/role'

    role_data = {
        'role_name': u'研发组',
        'permission_ids': '1,3',
    }

    role_name_2 = u'Test Leader'

    role_data_2 = {
        'role_name': u'Test Leader',
        'permission_ids': '1,2',
    }

    def test_create(self, user, testapp, client, db):
        """create successful."""
        # 1.create another role
        resp = client.post('%s/' % (self.uri_prefix), data=self.role_data)

        response_success(resp)
        compare_req_resp(self.role_data, resp)

        # 2.create another role
        resp = client.post('%s/' % (self.uri_prefix), data=self.role_data_2)

        response_success(resp)
        compare_req_resp(self.role_data_2, resp)

    def test_one(self, user, testapp, client, db):
        """item successful."""
        # Goes to homepage
        resp = client.get('%s/%d' % (self.uri_prefix, 1))

        response_success(resp)
        compare_req_resp(self.role_data, resp)

    def test_get_list_page_size(self, user, testapp, client):
        """test list should create 2 users at least, due to test pagination, searching."""

        query = {
            'page': 1,
            'size': 1,
        }
        response = {
            'count': 2,
        }
        resp = client.get('%s/?%s' % (self.uri_prefix, urllib.urlencode(query)))
        response_success(resp)
        resp_dict = resp_json(resp)

        compare_in(self.role_data_2, resp_dict['data']['list'].pop())
        compare_req_resp(response, resp)

    def test_get_list_query(self, user, testapp, client):
        """test list should create 2 users at least, due to test pagination, searching."""
        query = {
            'page': 1,
            'size': 1,
            'kw': self.role_name_2
        }
        response = {
            'count': 1,
        }
        resp = client.get('%s/?%s' % (self.uri_prefix, urllib.urlencode(query)))
        response_success(resp)
        resp_dict = resp_json(resp)

        compare_in(self.role_data_2, resp_dict['data']['list'].pop())
        compare_req_resp(response, resp)

    def test_get_update(self, user, testapp, client):
        """Login successful."""
        # 1.create another role
        resp = client.post('%s/' % (self.uri_prefix), data=self.role_data)
        role_id = resp_json(resp)['data']['id']

        response_success(resp)
        compare_req_resp(self.role_data, resp)

        # 2.update
        resp = client.put('%s/%d' % (self.uri_prefix, role_id), data=self.role_data_2)

        response_success(resp)
        compare_req_resp(self.role_data_2, resp)

        # 3.get it
        resp = client.get('%s/%d' % (self.uri_prefix, role_id))
        response_success(resp)
        compare_req_resp(self.role_data_2, resp)

    def test_get_remove(self, user, testapp, client):
        """Login successful."""
        # 1.create another role
        resp = client.post('%s/' % (self.uri_prefix), data=self.role_data)
        role_id = resp_json(resp)['data']['id']

        response_success(resp)
        compare_req_resp(self.role_data, resp)

        # 2.delete
        role_data_2 = self.role_data
        role_data_2['role_name'] = 'Test Leader'
        resp = client.delete('%s/%d' % (self.uri_prefix, role_id), data=role_data_2)

        # 3.get it
        resp = client.get('%s/%d' % (self.uri_prefix, role_id))
        response_error(resp)
