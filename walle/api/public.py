# -*- coding: utf-8 -*-
"""

    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-25 11:15:01
    :author: wushuiyong@walle-web.io
"""

import os

from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename

from walle.common.controller import Controller
from walle.model.user import UserModel
from walle.model.user import AccessModel
from walle.service.rbac.access import Access


class PublicAPI(Resource):
    def get(self, method):
        """
        fetch role list or one role

        :return:
        """
        if method == 'menu':
            return self.menu()

    def post(self, method):
        """
        fetch role list or one role

        :return:
        """
        if method == 'avater':
            return self.avater()

    def menu(self):
        user = UserModel(id=1).item()
        menu = AccessModel().menu('x')
        data = {
            'user': user,
            'menu': menu,
        }
        return Controller.render_json(data=data)

    def avater(self):
        UPLOAD_FOLDER = 'fe/public/avater'
        f = request.files['avater']
        fname = secure_filename(f.filename)
        # todo rename to uid relation
        fname = secure_filename(f.filename)
        ret = f.save(os.path.join(UPLOAD_FOLDER, fname))

        return Controller.render_json(data={
            'avarter': fname,
        })
