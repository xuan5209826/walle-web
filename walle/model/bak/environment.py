#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

from sqlalchemy import String, Integer, DateTime

# from flask_cache import Cache
from datetime import datetime

from walle.model.database import db


# from walle.service.rbac import access as rbac


# 环境级别
class EnvironmentModel(db.Model):
    # 表的名字:
    __tablename__ = 'environment'

    status_open = 1
    status_close = 2
    current_time = datetime.now()

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(20))
    status = db.Column(Integer)
    created_at = db.Column(DateTime, default=current_time)
    updated_at = db.Column(DateTime, default=current_time, onupdate=current_time)

    def list(self, page=0, size=10, kw=None):
        """
        获取分页列表
        :param page:
        :param size:
        :param kw:
        :return:
        """
        query = self.query
        if kw:
            query = query.filter(EnvironmentModel.name.like('%' + kw + '%'))
        count = query.count()

        data = query.order_by('id desc').offset(int(size) * int(page)).limit(size).all()
        env_list = [p.to_json() for p in data]
        return env_list, count

    def item(self, env_id=None):
        """
        获取单条记录
        :param role_id:
        :return:
        """
        data = self.query.filter_by(id=self.id).first()
        return data.to_json() if data else []

    def add(self, env_name):
        # todo permission_ids need to be formated and checked
        env = EnvironmentModel(name=env_name, status=self.status_open)

        db.session.add(env)
        db.session.commit()
        if env.id:
            self.id = env.id

        return env.id

    def update(self, env_name, status, env_id=None):
        # todo permission_ids need to be formated and checked
        role = EnvironmentModel.query.filter_by(id=self.id).first()
        role.name = env_name
        role.status = status

        return db.session.commit()

    def remove(self, env_id=None):
        """

        :param role_id:
        :return:
        """
        self.query.filter_by(id=self.id).delete()
        return db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'status': self.status,
            'env_name': self.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
