#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

import json
from sqlalchemy import Column, String, Integer, create_engine, Text, DateTime, desc, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import jsonify

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask.ext.login import UserMixin
from pickle import dump

# from flask.ext.cache import Cache
from datetime import datetime
import time

db = SQLAlchemy()


# 上线单
class Task(db.Model):
    # 表的名字:
    __tablename__ = 'task'

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer)
    project_id = db.Column(Integer)
    action = db.Column(Integer)
    status = db.Column(Integer)
    title = db.Column(String(100))
    link_id = db.Column(String(100))
    ex_link_id = db.Column(String(100))
    servers = db.Column(Text)
    commit_id = db.Column(String(40))
    branch = db.Column(String(100))
    file_transmission_mode = db.Column(Integer)
    file_list = db.Column(Text)
    enable_rollback = db.Column(Integer)
    created_at = db.Column(DateTime)
    updated_at = db.Column(DateTime)

    taskMdl = None

    def __init__(self, task_id=None):
        if task_id:
            self.id = task_id
            self.taskMdl = Task.query.filter_by(id=self.id).one().to_json()

    def table_name(self):
        return self.__tablename__

    def __repr__(self):
        return '<User %r>' % (self.title)

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'action': self.action,
            'status': self.status,
            'title': self.title,
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

    def list(self, page=0, size=10):
        data = Task.query.order_by('id').offset(int(size) * int(page)).limit(size).all()
        return [p.to_json() for p in data]

    def one(self):
        project_info = Project.query.filter_by(id=self.taskMdl.get('project_id')).one().to_json()
        return dict(project_info, **self.taskMdl)


# 上线记录表
class TaskRecord(db.Model):
    # 表的名字:
    __tablename__ = 'task_record'

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    stage = db.Column(String(20))
    sequence = db.Column(Integer)
    user_id = db.Column(Integer)
    task_id = db.Column(Integer)
    status = db.Column(Integer)
    command = db.Column(String(200))
    success = db.Column(String(2000))
    error = db.Column(String(2000))

    def save_record(self, stage, sequence, user_id, task_id, status, command, success, error):
        record = TaskRecord(stage=stage, sequence=sequence, user_id=user_id,
                            task_id=task_id, status=status, command=command,
                            success=success, error=error)
        db.session.add(record)
        return db.session.commit()


# 环境级别
class Environment(db.Model):
    # 表的名字:
    __tablename__ = 'environment'

    status_open = 1
    status_close = 2;

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(20))
    status = db.Column(Integer)

    def list(self, page=0, size=10, kw=None):
        """
        获取分页列表
        :param page:
        :param size:
        :return:
        """
        query = self.query
        if kw:
            query = query.filter(Environment.name.like('%' + kw + '%'))
        data = query.order_by('id desc').offset(int(size) * int(page)).limit(size).all()
        return [p.to_json() for p in data]

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
        env = Environment(name=env_name, status=self.status_open)

        db.session.add(env)
        return db.session.commit()

    def update(self, env_name, status, env_id=None):
        # todo permission_ids need to be formated and checked
        role = Environment.query.filter_by(id=self.id).first()
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
            'name': self.name,
        }


# 项目配置表
class Project(db.Model):
    # 表的名字:
    __tablename__ = 'project'

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer)
    name = db.Column(String(100))
    environment_id = db.Column(Integer)
    status = db.Column(Integer)
    version = db.Column(String(40))
    excludes = db.Column(Text)
    target_user = db.Column(String(50))
    target_root = db.Column(String(200))
    target_library = db.Column(String(200))
    servers = db.Column(Text)
    prev_deploy = db.Column(Text)
    post_deploy = db.Column(Text)
    prev_release = db.Column(Text)
    post_release = db.Column(Text)
    post_release_delay = db.Column(Integer)
    keep_version_num = db.Column(Integer)
    repo_url = db.Column(String(200))
    repo_username = db.Column(String(50))
    repo_password = db.Column(String(50))
    repo_mode = db.Column(String(50))
    repo_type = db.Column(String(10))

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'environment_id': self.environment_id,
            'status': self.status,
            'version': self.version,
            'excludes': self.excludes,
            'target_user': self.target_user,
            'target_root': self.target_root,
            'target_library': self.target_library,
            'servers': self.servers,
            'prev_deploy': self.prev_deploy,
            'post_deploy': self.post_deploy,
            'prev_release': self.prev_release,
            'post_release': self.post_release,
            'post_release_delay': self.post_release_delay,
            'keep_version_num': self.keep_version_num,
            'repo_url': self.repo_url,
            'repo_username': self.repo_username,
            'repo_password': self.repo_password,
            'repo_mode': self.repo_mode,
            'repo_type': self.repo_type,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


# 项目配置表
class User(db.Model, UserMixin):
    # 表的名字:
    __tablename__ = 'user'

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    password_hash = 'sadfsfkk'
    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    username = db.Column(String(50))
    is_email_verified = db.Column(Integer, default=0)
    email = db.Column(String(50), unique=True, nullable=False)
    password = db.Column(String(50), nullable=False)
    # password_hash = db.Column(String(50), nullable=False)
    avatar = db.Column(String(100))
    role_id = db.Column(Integer, default=0)
    status = db.Column(Integer, default=0)
    created_at = db.Column(DateTime, default=current_time)
    updated_at = db.Column(DateTime, default=current_time, onupdate=current_time)

    #
    # def __init__(self, email=None, password=None):
    #     from walle.common.tokens import TokenManager
    #     tokenManage = TokenManager()
    #     if email and password:
    #         self.email = email
    #         self.username = email
    #         self.password = tokenManage.generate_token(password)
    #         self.role_id = 0
    #         self.is_email_verified = 0
    #         self.status = 0
    #
    # @property
    # def password(self):
    #     """
    #     明文密码（只读）
    #     :return:
    #     """
    #     raise AttributeError(u'文明密码不可读')
    #
    #
    # @password_login.setter
    # def password_login(self, value):
    #     """
    #     写入密码，同时计算hash值，保存到模型中
    #     :return:
    #     """
    #     self.password = generate_password_hash(value)

    def item(self, user_id=None):
        """
        获取单条记录
        :param role_id:
        :return:
        """
        data = self.query.filter_by(id=self.id).first()
        return data.to_json() if data else []

    def update(self, username, role_id, password=None):
        # todo permission_ids need to be formated and checked
        user = self.query.filter_by(id=self.id).first()
        user.username = username
        user.role_id = role_id
        if password:
            user.password = generate_password_hash(password)

        db.session.commit()
        return user.to_json()

    def remove(self):
        """

        :param role_id:
        :return:
        """
        self.query.filter_by(id=self.id).delete()
        return db.session.commit()

    def verify_password(self, password):
        """
        检查密码是否正确
        :param password:
        :return:
        """
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def list(self, page=0, size=10, kw=None):
        """
        获取分页列表
        :param page:
        :param size:
        :return:
        """
        query = User.query
        if kw:
            query = query.filter(or_(User.username.like('%' + kw + '%'), User.email.like('%' + kw + '%')))
        data = query.order_by('id desc').offset(int(size) * int(page)).limit(size).all()
        return [p.to_json() for p in data]

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_email_verified': self.is_email_verified,
            'email': self.email,
            'avatar': self.avatar,
            'role_id': self.role_id,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


# 项目配置表
class Role(db.Model):
    # 表的名字:
    __tablename__ = 'role'

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(30))
    permission_ids = db.Column(Text, default='')
    created_at = db.Column(DateTime, default=current_time)
    updated_at = db.Column(DateTime, default=current_time, onupdate=current_time)

    def list(self, page=0, size=10, kw=None):
        """
        获取分页列表
        :param page:
        :param size:
        :return:
        """
        query = Role.query
        if kw:
            query = query.filter(Role.name.like('%' + kw + '%'))
        data = query.order_by('id desc').offset(int(size) * int(page)).limit(size).all()
        return [p.to_json() for p in data]

    def item(self, role_id):
        """
        获取单条记录
        :param role_id:
        :return:
        """
        data = Role.query.filter_by(id=role_id).first()
        return data.to_json() if data else []

    def add(self, name, permission_ids):
        # todo permission_ids need to be formated and checked
        role = Role(name=name, permission_ids=permission_ids)

        db.session.add(role)
        return db.session.commit()

    def update(self, id, name, permission_ids):
        # todo permission_ids need to be formated and checked
        role = Role.query.filter_by(id=id).first()
        role.name = name
        role.permission_ids = permission_ids

        return db.session.commit()

    def remove(self, role_id):
        """

        :param role_id:
        :return:
        """
        Role.query.filter_by(id=role_id).delete()
        return db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'permission_ids': self.permission_ids,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


# 项目配置表
class Tag(db.Model):
    # 表的名字:
    __tablename__ = 'tag'

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(30))
    label = db.Column(String(30))
    users = db.relationship('Group', backref='group', lazy='dynamic')
    created_at = db.Column(DateTime, default=current_time)
    updated_at = db.Column(DateTime, default=current_time, onupdate=current_time)

    def list(self):
        data = Tag.query.filter_by(id=1).first()
        f = open('aa.txt', 'w')
        dump(data.users.first().to_json(), f)
        # # return data.tag.count('*').to_json()
        # # print(data)
        # return []
        return data.to_json() if data else []

    def remove(self, tag_id):
        """

        :param role_id:
        :return:
        """
        Tag.query.filter_by(id=tag_id).delete()
        return db.session.commit()

    def to_json(self):
        user_ids = []
        for user in self.users.all():
            user_ids.append(user.user_id)
        return {
            'id': self.id,
            'name': self.name,
            'users': user_ids,
            'label': self.label,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


# 项目配置表
class Group(db.Model):
    # 表的名字:
    __tablename__ = 'user_group'

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, default=0)
    group_id = db.Column(Integer, db.ForeignKey('tag.id'))
    created_at = db.Column(DateTime, default=current_time)
    updated_at = db.Column(DateTime, default=current_time, onupdate=current_time)

    def list(self, page=0, size=10, kw=None):
        """
        获取分页列表
        :param page:
        :param size:
        :return:
        """
        query = Tag.query
        if kw:
            query = query.filter(Tag.name.like('%' + kw + '%'))
        data = query.order_by('id desc').offset(int(size) * int(page)).limit(size).all()
        return [p.to_json() for p in data]

    def add(self, group_name, user_ids):
        tag = Tag(name=group_name, label='user_group')
        db.session.add(tag)
        db.session.commit()

        for user_id in user_ids:
            user_group = Group(group_id=tag.id, user_id=user_id)
            db.session.add(user_group)

        db.session.commit()
        return tag.to_json()

    def update(self, group_id, group_name, user_ids):
        # 修改tag信息
        tag_model = Tag.query.filter_by(label='user_group').filter_by(id=group_id).first()
        if tag_model.name != group_name:
            tag_model.name = group_name

        # 修改用户组成员
        group_model = Group.query.filter_by(group_id=group_id).all()
        user_exists = []
        for group in group_model:
            # 用户组的用户id
            user_exists.append(group.user_id)
            # 表里的不在提交中,删除之
            if group.user_id not in user_ids:
                Group.query.filter_by(id=group.id).delete()

        # 提交的不在表中的,添加之
        user_not_in = list(set(user_ids).difference(set(user_exists)))
        for user_new in user_not_in:
            group_new = Group(group_id=group_id, user_id=user_new)
            db.session.add(group_new)

        db.session.commit()
        return self.item()

    def item(self):
        """
        获取单条记录
        :param role_id:
        :return:
        """

        data = Tag.query.filter_by(id=self.group_id).first()
        return data.to_json() if data else []

    def remove(self, group_id=None, user_id=None):
        """

        :param role_id:
        :return:
        """
        if group_id:
            Group.query.filter_by(group_id=group_id).delete()
        elif user_id:
            Group.query.filter_by(user_id=user_id).delete()
        elif self.group_id:
            Group.query.filter_by(group_id=self.group_id).delete()

        return db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'group_id': self.group_id,
            'group_name': self.group.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
