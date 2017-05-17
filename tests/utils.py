# -*- coding: utf-8 -*-
"""
    walle-web

    reference to https://github.com/closeio/flask-mongorest
    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-05-17 07:35:48
    :author: wushuiyong@walle-web.io
"""

import json
import copy
import datetime
import unittest
import walle


def response_success(response, code=None):
    f = open('log', 'w')
    f.write(str(response))
    if code is None:
        assert 200 <= response.status_code < 300, 'Received %d response: %s' % (response.status_code, response.data)
    else:
        assert code == response.status_code, 'Received %d response: %s' % (response.status_code, response.data)


def response_error(response, code=None):
    if code is None:
        assert 400 <= response.status_code < 500, 'Received %d response: %s' % (response.status_code, response.data)
    else:
        assert code == response.status_code, 'Received %d response: %s' % (response.status_code, response.data)


def compare_req_resp(req_obj, resp_obj):
    for k, v in req_obj.items():
        assert k in resp_obj.keys(), 'Key %r not in response (keys are %r)' % (k, resp_obj.keys())
        assert resp_obj[k] == v, 'Value for key %r should be %r but is %r' % (k, v, resp_obj[k])


def resp_json(resp):
    return json.loads(resp.get_data(as_text=True))
