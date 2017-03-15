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

    taskMdl=None

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
    id = db.Column(Integer, primary_key=True)
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
class enviroment(db.Model):
    # 表的名字:
    __tablename__ = 'enviroment'

    # 表的结构:
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(20))
    status = db.Column(Integer)

# 项目配置表
class Project(db.Model):
    # 表的名字:
    __tablename__ = 'project'

    # 表的结构:
    id = db.Column(Integer, primary_key=True)
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
        }