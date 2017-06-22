# -*- coding: utf-8 -*-
"""

    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-03-25 11:15:01
    :author: wushuiyong@walle-web.io
"""

from flask import request
from walle.api.api import SecurityResource
from walle.form.task import TaskForm
from walle.model.deploy import TaskModel


class TaskAPI(SecurityResource):
    def get(self, task_id=None):
        """
        fetch project list or one item
        /project/<int:project_id>
        :return:
        """
        super(TaskAPI, self).get()

        return self.item(task_id) if task_id else self.list()

    def list(self):
        """
        fetch project list
        :return:
        """
        page = int(request.args.get('page', 0))
        page = page - 1 if page else 0
        size = float(request.args.get('size', 10))
        kw = request.values.get('kw', '')

        task_model = TaskModel()
        task_list, count = task_model.list(page=page, size=size, kw=kw)
        return self.list_json(list=task_list, count=count)

    def item(self, task_id):
        """
        获取某个用户组
        :param id:
        :return:
        """

        task_model = TaskModel(id=task_id)
        task_info = task_model.item()
        if not task_info:
            return self.render_json(code=-1)
        return self.render_json(data=task_info)

    def post(self):
        """
        create a environment
        /environment/
        :return:
        """
        super(TaskAPI, self).post()

        form = TaskForm(request.form, csrf_enabled=False)
        # return self.render_json(code=-1, data = form.form2dict())
        if form.validate_on_submit():
            task_new = TaskModel()
            data = form.form2dict()
            id = task_new.add(data)
            if not id:
                return self.render_json(code=-1)

            return self.render_json(data=task_new.item())
        else:
            return self.render_json(code=-1, message=form.errors)

    def put(self, task_id):
        """
        update environment
        /environment/<int:id>
        :return:
        """
        super(TaskAPI, self).put()

        form = TaskForm(request.form, csrf_enabled=False)
        f = open('run.log', 'w')
        form.set_id(task_id)
        if form.validate_on_submit():
            task = TaskModel().get_by_id(task_id)
            data = form.form2dict()
            f.write('\n====form2dict===\n' + str(data))
            # a new type to update a model
            ret = task.update(data)
            return self.render_json(data=task.item())
        else:
            return self.render_json(code=-1, message=form.errors)

    def delete(self, task_id):
        """
        remove an environment
        /environment/<int:id>
        :return:
        """
        super(TaskAPI, self).delete()

        task_model = TaskModel(id=task_id)
        task_model.remove(task_id)

        return self.render_json(message='')
