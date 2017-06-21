#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

from sqlalchemy import String, Integer, DateTime

# from flask_cache import Cache
from datetime import datetime
from walle.model.database import SurrogatePK, db, Model


# server
class ServerModel(SurrogatePK, Model):
    __tablename__ = 'server'

    current_time = datetime.now()

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(100))
    host = db.Column(String(100))
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
            query = query.filter(ServerModel.name.like('%' + kw + '%'))
        count = query.count()

        data = query.order_by('id desc') \
            .offset(int(size) * int(page)).limit(size) \
            .all()
        server_list = [p.to_json() for p in data]
        return server_list, count

    def item(self, id=None):
        """
        获取单条记录
        :param role_id:
        :return:
        """
        id = id if id else self.id
        data = self.query.filter_by(id=id).first()
        return data.to_json() if data else []

    def add(self, name, host):
        # todo permission_ids need to be formated and checked
        server = ServerModel(name=name, host=host)

        db.session.add(server)
        db.session.commit()
        if ServerModel.id:
            self.id = ServerModel.id

        return ServerModel.id

    def update(self, name, host, id=None):
        # todo permission_ids need to be formated and checked
        id = id if id else self.id
        role = ServerModel.query.filter_by(id=id).first()

        if not role:
            return False

        role.name = name
        role.host = host

        return db.session.commit()

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
            'host': self.host,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
