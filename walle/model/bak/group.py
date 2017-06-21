#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

from sqlalchemy import Integer, DateTime

# from flask_cache import Cache
from datetime import datetime

from walle.model.database import SurrogatePK, db, Model
from walle.model.tag import TagModel


class GroupModel(SurrogatePK, Model):
    __tablename__ = 'user_group'

    current_time = datetime.now()

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, db.ForeignKey('user.id'))
    user_ids = db.relationship('TagModel', backref=db.backref('users'))
    group_id = db.Column(Integer, db.ForeignKey('tag.id'))
    created_at = db.Column(DateTime, default=current_time)
    updated_at = db.Column(DateTime, default=current_time, onupdate=current_time)
    group_name = None

    def list(self, page=0, size=10, kw=None):
        """
        获取分页列表
        :param page:
        :param size:
        :return:
        """
        group = GroupModel.query
        if kw:
            group = GroupModel.filter_by(TagModel.name.like('%' + kw + '%'))
        group = GroupModel.offset(int(size) * int(page)).limit(size).all()
        # f = open('run.log', 'w')
        # f.write('==group_id==\n'+str(group_id)+'\n====\n')

        list = [p.to_json() for p in group]
        return list, 3

        user_ids = []
        group_dict = {}
        for group_info in group:
            user_ids.append(group_info.user_id)
            group_dict = group_info.to_json()

        group_dict['user_ids'] = user_ids
        # del group_dict['user_id']
        # return user_ids
        return group_dict

        query = TagModel.query
        if kw:
            query = query.filter(Tag.name.like('%' + kw + '%'))
        count = query.count()
        data = query.order_by('id desc').offset(int(size) * int(page)).limit(size).all()
        list = [p.to_json() for p in data]
        return list, count

    def add(self, group_name, user_ids):
        tag = TagModel(name=group_name, label='user_group')
        db.session.add(tag)
        db.session.commit()

        for user_id in user_ids:
            user_group = GroupModel(group_id=tag.id, user_id=user_id)
            db.session.add(user_group)

        db.session.commit()
        if tag.id:
            self.group_id = tag.id

        return tag.id

    def update(self, group_id, group_name, user_ids):
        # 修改tag信息
        tag_model = TagModel.query.filter_by(label='user_group').filter_by(id=group_id).first()
        if tag_model.name != group_name:
            tag_model.name = group_name

        # 修改用户组成员
        group_model = GroupModel.query.filter_by(group_id=group_id).all()
        user_exists = []
        for group in group_model:
            # 用户组的用户id
            user_exists.append(GroupModel.user_id)
            # 表里的不在提交中,删除之
            if GroupModel.user_id not in user_ids:
                GroupModel.query.filter_by(id=GroupModel.id).delete()

        # 提交的不在表中的,添加之
        user_not_in = list(set(user_ids).difference(set(user_exists)))
        for user_new in user_not_in:
            group_new = GroupModel(group_id=group_id, user_id=user_new)
            db.session.add(group_new)

        db.session.commit()
        return self.item()

    def item(self, group_id=None):
        """
        获取单条记录
        :param role_id:
        :return:
        """
        #
        group_id = group_id if group_id else self.group_id
        tag = TagModel.query.filter_by(id=group_id).first()
        if not tag:
            return None
        tag = tag.to_json()

        group_id = group_id if group_id else self.group_id
        groups = GroupModel.query.filter_by(group_id=group_id).all()

        user_ids = []
        for group_info in groups:
            user_ids.append(group_info.user_id)

        tag['user_ids'] = user_ids
        tag['users'] = len(user_ids)
        return tag

        del group_dict['user_id']
        # return user_ids
        return group_dict
        return GroupModel.to_json()
        # group = GroupModel.to_json()

        users = User.query \
            .filter(User.id.in_(group['users'])).all()
        group['user_ids'] = [user.to_json() for user in users]

        return group

    def remove(self, group_id=None, user_id=None):
        """

        :param role_id:
        :return:
        """
        if group_id:
            GroupModel.query.filter_by(group_id=group_id).delete()
        elif user_id:
            GroupModel.query.filter_by(user_id=user_id).delete()
        elif self.group_id:
            GroupModel.query.filter_by(group_id=self.group_id).delete()

        return db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'group_id': self.group_id,
            'group_name': self.group_name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


class Foo(SurrogatePK, Model):
    __tablename__ = 'foo'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
