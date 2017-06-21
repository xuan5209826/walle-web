#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

from flask_login import UserMixin
from sqlalchemy import String, Integer, Text, DateTime

# from flask_cache import Cache
from datetime import datetime
from walle.model.database import SurrogatePK, db, relationship, Model
# from walle.model.user import UserModel


# 项目配置表
class RoleModel(UserMixin, SurrogatePK, Model):
    # 表的名字:
    __tablename__ = 'role'

    # current_time = datetime.now()
    current_time = datetime.now()

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(30))
    access_ids = db.Column(Text, default='')
    users = relationship("UserModel", back_populates="role_info")

    created_at = db.Column(DateTime, default=current_time)
    updated_at = db.Column(DateTime, default=current_time, onupdate=current_time)

    def list(self, page=0, size=10, kw=None):
        """
        获取分页列表
        :param page:
        :param size:
        :return:
        """
        query = RoleModel.query
        if kw:
            query = query.filter(RoleModel.name.like('%' + kw + '%'))
        count = query.count()
        data = query.order_by('id desc').offset(int(size) * int(page)).limit(size).all()
        list = [p.to_json() for p in data]
        return list, count

    def item(self, role_id=None):
        """
        获取单条记录
        :param role_id:
        :return:
        """
        role_id = role_id if role_id else self.id
        data = RoleModel.query.filter_by(id=role_id).first()
        return data.to_json() if data else []

    def add(self, name, access_ids):
        # todo access_ids need to be formated and checked
        role = RoleModel(name=name, access_ids=access_ids)

        db.session.add(role)
        db.session.commit()
        self.id = RoleModel.id
        return self.id

    def update(self, name, access_ids, role_id=None):
        # todo access_ids need to be formated and checked
        role_id = role_id if role_id else self.id
        role = RoleModel.query.filter_by(id=role_id).first()
        RoleModel.name = name
        RoleModel.access_ids = access_ids

        return db.session.commit()

    def remove(self, role_id=None):
        """

        :param role_id:
        :return:
        """
        role_id = role_id if role_id else self.id
        RoleModel.query.filter_by(id=role_id).delete()
        return db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'role_name': self.name,
            'access_ids': self.access_ids,
            'users': len(self.users),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
