# -*- coding: utf-8 -*-
"""Test Apis."""
from flask import json
import types
import urllib
import pytest
from utils import *


@pytest.mark.usefixtures('db')
class TestApiGroup:
    """api role testing"""
    uri_prefix = '/api/group'

    user_id = {}

    group_data = {
        'group_name': u'测试组',
        'user_ids': u'1,2',
        'users': 2,
    }

    group_name_2 = u'Developer'

    group_data_2 = {
        'group_name': u'Developer',
        'user_ids': u'1',
        'users': 1,
    }

    group_data_remove = {
        'group_name': u'group_remove',
        'user_ids': u'1,2',
        'users': 2,
    }

    def test_create(self, user, testapp, client, db):
        """create successful."""
        # 1.create another role
        resp = client.post('%s/' % (self.uri_prefix), data=self.group_data)
        # f = open('run.log', 'w')
        # f.write('\n==test_create==\n'+str(resp.data))

        group_data = self.get_list_ids(self.group_data)
        response_success(resp)
        compare_req_resp(group_data, resp)

        self.group_data['group_id'] = resp_json(resp)['data']['group_id']

        # 2.create another group
        resp = client.post('%s/' % (self.uri_prefix), data=self.group_data_2)
        group_data_2 = self.get_list_ids(self.group_data_2)

        response_success(resp)
        compare_req_resp(group_data_2, resp)
        self.group_data_2['group_id'] = resp_json(resp)['data']['group_id']


    def test_one(self, user, testapp, client, db):
        """item successful."""
        # Goes to homepage

        resp = client.get('%s/%d' % (self.uri_prefix, self.group_data['group_id']))
        # f = open('run.log', 'w')
        # f.write('\n==test_one==\n'+str(resp.data))
        group_data = self.get_list_ids(self.group_data)

        response_success(resp)
        compare_req_resp(group_data, resp)

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
        # f = open('run.log', 'w')
        # f.write('%s/%d' % (self.uri_prefix, self.group_data['group_id']))
        # f.write(str(self.group_data_2))

        res = resp_dict['data']['list'].pop()
        # f.write(str(res))

        # compare_in(self.group_data_2, resp_dict['data']['list'].pop())
        group_data_2 = self.get_list_ids(self.group_data_2)
        del group_data_2['user_ids']

        compare_in(group_data_2, res)
        compare_req_resp(response, resp)
    
    def test_get_list_query(self, user, testapp, client):
        """test list should create 2 users at least, due to test pagination, searching."""
        query = {
            'page': 1,
            'size': 1,
            'kw': self.group_name_2
        }
        response = {
            'count': 1,
        }
        resp = client.get('%s/?%s' % (self.uri_prefix, urllib.urlencode(query)))
        response_success(resp)
        resp_dict = resp_json(resp)
        group_data_2 = self.get_list_ids(self.group_data_2)
        del group_data_2['user_ids']

        compare_in(group_data_2, resp_dict['data']['list'].pop())
        compare_req_resp(response, resp)
    
    def test_get_update(self, user, testapp, client):
        """Login successful."""
        # 1.update
        group_data_2 = self.group_data_2
        group_data_2['group_name'] = u'中文Tester_edit'
        resp = client.put('%s/%d' % (self.uri_prefix, self.group_data_2['group_id']), data=group_data_2)

        group_data_2 = self.get_list_ids(group_data_2)

        response_success(resp)
        compare_req_resp(group_data_2, resp)
    
        # 3.get it
        resp = client.get('%s/%d' % (self.uri_prefix, self.group_data_2['group_id']))
        response_success(resp)
        compare_req_resp(group_data_2, resp)
    
    def test_get_remove(self, user, testapp, client):
        """Login successful."""
        # 1.create another role
        resp = client.post('%s/' % (self.uri_prefix), data=self.group_data_remove)
        group_id = resp_json(resp)['data']['group_id']
        response_success(resp)
    
        # 2.delete
        resp = client.delete('%s/%d' % (self.uri_prefix, group_id))
        response_success(resp)
    
        # 3.get it
        resp = client.get('%s/%d' % (self.uri_prefix, group_id))
        response_error(resp)
    
    def get_list_ids(self, groupOrigin):
        group_list = groupOrigin.copy()
        group_list['user_ids'] = map(int, groupOrigin['user_ids'].split(','))
        return group_list