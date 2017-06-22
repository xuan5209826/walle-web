# -*- coding: utf-8 -*-
"""

    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-25 11:15:01
    :author: wushuiyong@walle-web.io
"""

from flask import request
from walle.api.api import SecurityResource
from walle.model.user import RoleModel


class RoleAPI(SecurityResource):
    """
    角色没有上下级, 一个角色的用户可以看到
    1.超管
    2.研发总监, 产品总监
    3.FE Leader, QA Leader, RD Leader
    4.FE 1, FE 2, FE 3

    场景：
    1.项目管理:下级角色建立的项目,上级是否可见可写
    2.上线单管理：下级角色提交的上线单，上级是否可以操作
    """

    def get(self, role_id=None):
        """
        fetch role list or one role

        :return:
        """
        super(RoleAPI, self).get()

        return self.item(role_id) if role_id else self.list()

    def list(self):
        """
        fetch role list
        /role/

        :return:
        """
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')

        role_model = RoleModel()
        role_list, count = role_model.list(page=page, size=size, kw=kw)
        return self.list_json(list=role_list, count=count)

    def item(self, role_id):
        """
        fetch one role
        /role/<int:role_id>

        :param role_id:
        :return:
        """
        role_model = RoleModel(id=role_id)
        role_info = role_model.item()
        if not role_info:
            return self.render_json(code=-1)
        return self.render_json(data=role_info)

    def post(self):
        """
        新增角色
        /role/

        :return:
        """
        super(RoleAPI, self).post()

        role_name = request.form.get('role_name', None)
        role_permissions_ids = request.form.get('access_ids', '')
        role_model = RoleModel()
        role_id = role_model.add(name=role_name, access_ids=role_permissions_ids)

        if not role_id:
            self.render_json(code=-1)
        return self.render_json(data=role_model.item())

    def put(self, role_id):
        """
        修改角色
        /role/<int:role_id>

        :param role_id:
        :return:
        """
        super(RoleAPI, self).put()

        role_name = request.form.get('role_name', None)
        role_access_ids = request.form.get('access_ids', '')

        if not role_name:
            return self.render_json(code=-1, message='role_name can not be empty')

        role_model = RoleModel(id=role_id)
        ret = role_model.update(name=role_name, access_ids=role_access_ids)
        return self.render_json(data=role_model.item())

    def delete(self, role_id):
        """
        删除一个角色
        /role/<int:role_id>

        :return:
        """
        super(RoleAPI, self).delete()

        role_model = RoleModel(id=role_id)
        ret = role_model.remove()

        return self.render_json(code=0)
