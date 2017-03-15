#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类:
Base = declarative_base()

# 上线记录表
class task_record(Base):
    # 表的名字:
    __tablename__ = 'task_record'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    stage = Column(String(20))
    sequence = Column(Integer)
    user_id = Column(Integer)
    task_id = Column(Integer)
    status = Column(Integer)
    command = Column(String(200))
    success = Column(String(2000))
    error = Column(String(2000))

# 环境级别
class enviroment(Base):
    # 表的名字:
    __tablename__ = 'enviroment'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    status = Column(Integer)

# 项目配置表
class project(Base):
    # 表的名字:
    __tablename__ = 'project'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    user_id = Column(String())
    name = Column(String())
    environment_id = Column(String())
    status = Column(String())
    version = Column(String())
    excludes = Column(String())
    target_user = Column(String())
    target_root = Column(String())
    target_library = Column(String())
    servers = Column(String())
    prev_deploy = Column(String())
    post_deploy = Column(String())
    prev_release = Column(String())
    post_release = Column(te)
    post_release_delay = Column(String())
    keep_version_num = Column(String())
    repo_url = Column(String())
    repo_username = Column(String())
    repo_password = Column(String())
    repo_mode = Column(String())
    repo_type = Column(String())
