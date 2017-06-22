# -*- coding: utf-8 -*-
"""

    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-25 11:15:01
    :author: wushuiyong@walle-web.io
"""

from flask import request
from werkzeug.security import generate_password_hash
from walle.form.user import UserUpdateForm, RegistrationForm
from walle.model.database import db
from walle.model.user import UserModel
from walle.model.user import GroupModel
from walle.model.tag import TagModel
from walle.api.api import SecurityResource


class UserAPI(SecurityResource):
    def get(self, user_id=None):
        """
        fetch user list or one user
        /user/<int:user_id>

        :return:
        """
        super(UserAPI, self).get()

        return self.item(user_id) if user_id else self.list()

    def list(self):
        """
        fetch user list or one user

        :return:
        """
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')

        user_model = UserModel()
        user_list, count = user_model.list(page=page, size=size, kw=kw)
        return self.list_json(list=user_list, count=count)

    def item(self, user_id):
        """
        获取某个用户

        :param user_id:
        :return:
        """

        user_info = UserModel(id=user_id).item()
        if not user_info:
            return self.render_json(code=-1)
        return self.render_json(data=user_info)

    def post(self):
        """
        create user
        /user/

        :return:
        """
        super(UserAPI, self).post()

        form = RegistrationForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            password = generate_password_hash(form.password.data)
            user = UserModel(email=form.email.data,
                             username=form.username.data,
                             password=password,
                             role_id=form.role_id.data
                             )
            db.session.add(user)
            db.session.commit()
            return self.render_json(data=user.item(user_id=user.id))
        return self.render_json(code=-1, message=form.errors)

    def put(self, user_id):
        """
        edit user
        /user/<int:user_id>

        :return:
        """
        super(UserAPI, self).put()

        form = UserUpdateForm(request.form, csrf_enabled=False)
        if form.validate_on_submit():
            user = UserModel(id=user_id)
            user.update(username=form.username.data, role_id=form.role_id.data, password=form.password.data)
            return self.render_json(data=user.item())

        return self.render_json(code=-1, message=form.errors)

    def delete(self, user_id):
        """
        remove a user with his group relation
        /user/<int:user_id>

        :param user_id:
        :return:
        """
        super(UserAPI, self).delete()

        UserModel(id=user_id).remove()
        GroupModel().remove(user_id=user_id)
        return self.render_json(message='')
