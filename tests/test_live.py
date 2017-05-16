# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-05-15 23:45:34
    :author: wushuiyong@walle-web.io
"""
import urllib2
from flask import Flask
from flask.ext.testing import LiveServerTestCase


# Testing with LiveServer
class MyTest(LiveServerTestCase):
    # if the create_app is not implemented NotImplementedError will be raised
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 5000
        return app

    def test_flask_application_is_up_and_running(self):
        f=open('/Users/wushuiyong/workspace/meolu/walle-web-python/tests/o.txt', 'w')
        f.write(self.get_server_url())
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    def test_flask_api_data(self):
        response = urllib2.urlopen(self.get_server_url())
        f=open('/Users/wushuiyong/workspace/meolu/walle-web-python/tests/o.txt', 'w')
        f.write(str(response))
        print(response)
        self.assertEqual(response.data, 'walle-web 2.0')

    # def test_some_json(self):
    #     response = self.client.get("/")
    #     self.assertEquals(response.data, 'walle-web 2.0')