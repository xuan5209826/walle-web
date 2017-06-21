#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

from sqlalchemy import String, Integer, Text, DateTime

# from flask_cache import Cache
from datetime import datetime

from walle.model.database import SurrogatePK, db, Model
from walle.model.project import ProjectModel


# from walle.service.rbac import access as rbac


moderators = db.Table(
    'moderators',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id'),
              nullable=False),
    db.Column('user_id', db.Integer(),
              db.ForeignKey('forums.id', use_alter=True, name="fk_forum_id"),
              nullable=False))

# 上线单
class TaskModel(SurrogatePK, Model):
    __tablename__ = 'task'
    current_time = datetime.now()

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(100))
    user_id = db.Column(Integer)
    project_id = db.Column(Integer)
    action = db.Column(Integer)
    status = db.Column(Integer)
    link_id = db.Column(String(100))
    ex_link_id = db.Column(String(100))
    servers = db.Column(Text)
    commit_id = db.Column(String(40))
    branch = db.Column(String(100))
    file_transmission_mode = db.Column(Integer)
    file_list = db.Column(Text)
    enable_rollback = db.Column(Integer)
    created_at = db.Column(DateTime, default=current_time)
    updated_at = db.Column(DateTime, default=current_time, onupdate=current_time)


    # Many-to-many
    moderators = db.relationship(
        "User",
        secondary=moderators,
        primaryjoin=(moderators.c.forum_id == id),
        backref=db.backref("forummoderator", lazy="dynamic"),
        lazy="joined"
    )

    taskMdl = None

    def table_name(self):
        return self.__tablename__

    #
    # def list(self, page=0, size=10, kw=''):
    #     data = Task.query.order_by('id').offset(int(size) * int(page)).limit(size).all()
    #     return [p.to_json() for p in data]
    #
    # def one(self):
    #     project_info = Project.query.filter_by(id=self.taskMdl.get('project_id')).one().to_json()
    #     return dict(project_info, **self.taskMdl)
    #

    def list(self, page=0, size=10, kw=None):
        """
        获取分页列表
        :param page:
        :param size:
        :param kw:
        :return:
        """
        query = TaskModel.query
        if kw:
            query = query.filter(TaskModel.name.like('%' + kw + '%'))
        count = query.count()

        data = query.order_by('id desc') \
            .offset(int(size) * int(page)).limit(size) \
            .all()
        task_list = []

        for task in data:
            task = task.to_json()
            project = ProjectModel().get_by_id(task['project_id']).to_dict()
            task['project_name'] = project['name'] if project else u'未知项目'
            task_list.append(task)

        return task_list, count

    def item(self, id=None):
        """
        获取单条记录
        :param role_id:
        :return:
        """
        id = id if id else self.id
        data = self.query.filter_by(id=id).first()
        if not data:
            return []

        task = data.to_json()
        project = ProjectModel().get_by_id(task['project_id']).to_dict()
        task['project_name'] = project['name'] if project else u'未知项目'
        return task

    def add(self, *args, **kwargs):
        # todo permission_ids need to be formated and checked
        data = dict(*args)
        f = open('run.log', 'w')
        f.write('\n====add===\n' + str(data))
        project = TaskModel(**data)

        db.session.add(project)
        db.session.commit()

        if project.id:
            self.id = project.id

        return project.id

    def update(self, *args, **kwargs):
        # todo permission_ids need to be formated and checked
        # a new type to update a model

        update_data = dict(*args)
        return super(TaskModel, self).update(**update_data)

    def remove(self, id=None):
        """

        :param role_id:
        :return:
        """
        id = id if id else self.id
        self.query.filter_by(id=id).delete()
        return db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': int(self.user_id),
            'project_id': int(self.project_id),
            'action': self.action,
            'status': self.status,
            'link_id': self.link_id,
            'ex_link_id': self.ex_link_id,
            'servers': self.servers,
            'commit_id': self.commit_id,
            'branch': self.branch,
            'file_transmission_mode': self.file_transmission_mode,
            'file_list': self.file_list,
            'enable_rollback': self.enable_rollback,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
