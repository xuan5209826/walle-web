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

# 定义User对象:
class task_record(Base):
    # 表的名字:
    __tablename__ = 'task_record'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    user_id = Column(String(20))
    task_id = Column(String(20))
    status = Column(String(20))
    command = Column(String(20))
    success = Column(String(20))
    error = Column(String(20))
