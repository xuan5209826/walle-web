# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-05-16 19:17:02
    :author: wushuiyong@walle-web.io
"""
import unittest
# import flaskapi
import walle
import requests
import json
from .utils import *

class MongoRestTestCase(unittest.TestCase):

    def setUp(self):
        self.user_true = {
            'email': 'test01@walle.com',
            'username': 'alan',
            'password': 'baker876$%',
            'role_id': '3',
        }

        self.user_false = {
            'email': 'test10@wallecom',
            'username': 'alan',
            'password': 'bakeradsf',
            'role_id': '3',
        }

        self.post_1 = {
            'title': 'first post!',
            #author
            #editor
            'tags': ['tag1', 'tag2', 'tag3'],
            #user_lists
            'sections': [
                {'text': 'this is the first section of the first post.',
                 'lang': 'en'},
                {'text': 'this is the second section of the first post.',
                 'lang': 'de'},
                {'text': 'this is the third section of the first post.',
                 'lang': 'fr'},
            ],
            'content': {
                'text': 'this is the content for my first post.',
                'lang': 'cn',
            },
            'is_published': True,
        }

        self.post_2 = {
            'title': 'Second post',
            'is_published': False,
        }

        self.client = walle.create_app().test_client()

        # # create user 1
        # resp = self.client.post('/user/', data=json.dumps(self.user_1))
        # response_success(resp)
        # self.user_1_obj = resp_json(resp)
        # compare_req_resp(self.user_1, self.user_1_obj)
        #
        # # create user 2
        # resp = self.client.post('/user/', data=json.dumps(self.user_2))
        # response_success(resp)
        # self.user_2_obj = resp_json(resp)
        # compare_req_resp(self.user_2, self.user_2_obj)

    def tearDown(self):
        pass
        # # delete user 1
        # resp = self.client.delete('/user/%s/' % self.user_1_obj['id'])
        # response_success(resp)
        # resp = self.client.get('/user/%s/' % self.user_1_obj['id'])
        # response_error(resp, code=404)
        #
        # # delete user 2
        # resp = self.client.delete('/user/%s/' % self.user_2_obj['id'])
        # response_success(resp)
        # resp = self.client.get('/user/%s/' % self.user_2_obj['id'])
        # response_error(resp, code=404)

    def test_update_user(self):
        # resp = self.client.post('/api/user/', data=json.dumps(self.user_true))
        resp = self.client.get('/api/user/')
        response_success(resp)

        # self.user_1_obj['first_name'] = 'anthony'
        # self.user_1_obj['datetime'] = datetime.datetime.utcnow().isoformat()
        # resp = self.client.put('/user/%s/' % self.user_1_obj['id'], data=json.dumps(self.user_1_obj))
        # response_success(resp)
        #
        # # check for request params in response, except for date (since the format will differ)
        # data_to_check = copy.copy(self.user_1_obj)
        # del data_to_check['datetime']
        # data = resp_json(resp)
        # compare_req_resp(data_to_check, data)
        #
        # # response from PUT should be completely identical as a subsequent GET
        # # (including precision of datetimes)
        # resp = self.client.get('/user/%s/' % self.user_1_obj['id'])
        # data2 = resp_json(resp)
        # self.assertEqual(data, data2)

    # def test_unicode(self):
    #     """
    #     Make sure unicode data payloads are properly decoded.
    #     """
    #     self.user_1_obj['first_name'] = u'Jörg'
    #
    #     # Don't encode unicode characters
    #     resp = self.client.put('/user/%s/' % self.user_1_obj['id'], data=json.dumps(self.user_1_obj, ensure_ascii=False))
    #     response_success(resp)
    #     data = resp_json(resp)
    #     compare_req_resp(self.user_1_obj, data)
    #
    #     # Encode unicode characters as "\uxxxx" (default)
    #     resp = self.client.put('/user/%s/' % self.user_1_obj['id'], data=json.dumps(self.user_1_obj, ensure_ascii=True))
    #     response_success(resp)
    #     data = resp_json(resp)
    #     compare_req_resp(self.user_1_obj, data)
    #
    # def test_model_validation_unicode(self):
    #     # MongoEngine validation error (no schema)
    #     resp = self.client.post('/test/', data=json.dumps({
    #         'email': u'💩',
    #     }))
    #     response_error(resp)
    #     errors = resp_json(resp)
    #     self.assertTrue(errors == {
    #         'field-errors': {
    #             'email': u'Invalid email address: 💩'
    #         }
    #     } or errors == {
    #         # Workaround for
    #         # https://github.com/MongoEngine/mongoengine/pull/1384
    #         'field-errors': {
    #             'email': u'Invalid email address: 💩'
    #         }
    #     })
    #
    #     # Schema validation error
    #     resp = self.client.post('/user/', data=json.dumps({
    #         'email': 'test@example.com',
    #         'datetime': 'invalid',
    #     }))
    #     response_error(resp)
    #     errors = resp_json(resp)
    #     self.assertEqual(errors, {
    #         'errors': [],
    #         'field-errors': {
    #             'datetime': u'Invalid date 💩'
    #         }
    #     })
    #
    # def test_model_validation(self):
    #     resp = self.client.post('/user/', data=json.dumps({
    #         'email': 'invalid',
    #         'first_name': 'joe',
    #         'last_name': 'baker',
    #         'datetime':'2012-08-13T05:25:04.362Z',
    #         'datetime_local':'2012-08-13T05:25:04.362-03:30'
    #     }))
    #     response_error(resp)
    #     errors = resp_json(resp)
    #     self.assertTrue('field-errors' in errors)
    #     self.assertEqual(set(errors['field-errors']), set(['email']))
    #
    #     resp = self.client.put('/user/%s/' % self.user_1_obj['id'], data=json.dumps({
    #         'email': 'invalid',
    #         'first_name': 'joe',
    #         'last_name': 'baker',
    #     }))
    #     response_error(resp)
    #     errors = resp_json(resp)
    #     self.assertTrue('field-errors' in errors)
    #     self.assertEqual(set(errors['field-errors']), set(['email']))
    #
    #     resp = self.client.put('/user/%s/' % self.user_1_obj['id'], data=json.dumps({
    #         'emails': ['one@example.com', 'invalid', 'second@example.com', 'invalid2'],
    #     }))
    #
    #     response_error(resp)
    #     errors = resp_json(resp)
    #     self.assertTrue('field-errors' in errors)
    #     self.assertEqual(set(errors['field-errors']), set(['emails']))
    #     self.assertEqual(set(errors['field-errors']['emails']['errors']), set(['1', '3']))

# class TestFlaskApiUsingRequests(unittest.TestCase):
#     def test_hello_world(self):
#         response = requests.get('http://localhost:5000')
#         self.assertEqual(response.text.strip(), '"walle-web 2.0"')

#
# class TestFlaskApi(unittest.TestCase):
#     def setUp(self):
#         self.client = walle.app.test_client()
#
#     def test_hello_world(self):
#         response = self.client.get('/api/role/')
#         self.assertEqual(json.loads(response.get_data()), {'hello': 'world'})


if __name__ == "__main__":
    unittest.main()