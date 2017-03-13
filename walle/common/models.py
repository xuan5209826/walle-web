#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

from sqlalchemy import Column, String, Integer, create_engine, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import current_user
# from flask.ext.cache import Cache
from datetime import *
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

# 上线记录表
class task_record(db.Model):
    # 表的名字:
    __tablename__ = 'task_record'

    # 表的结构:
    id = db.Column(Integer, primary_key=True)
    stage = db.Column(String(20))
    sequence = db.Column(Integer)
    user_id = db.Column(Integer)
    task_id = db.Column(Integer)
    status = db.Column(Integer)
    command = db.Column(String(200))
    success = db.Column(String(2000))
    error = db.Column(String(2000))

# 环境级别
class enviroment(db.Model):
    # 表的名字:
    __tablename__ = 'enviroment'

    # 表的结构:
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(20))
    status = db.Column(Integer)

# 项目配置表
class project(db.Model):
    # 表的名字:
    __tablename__ = 'project'

    # 表的结构:
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(20))
    user_id = db.Column(Integer)
    enviroment_id = db.Column(Integer)
    status = db.Column(Integer)
    version = db.Column(Integer)
    excludes = db.Column(String(200))
    success = db.Column(String(2000))
    error = db.Column(String(2000))

