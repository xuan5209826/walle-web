#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:
from model import task_record

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# 初始化数据库连接:
engine = create_engine('mysql://root:whoiam@localhost:3306/walle-python')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建Session:
session = DBSession()

# 创建新User对象:
new_record = task_record(
    user_id=1222,
    task_id=11,
    status=3,
    command='whoami',
    success='wushuiyong',
    error=''
)
# 添加到session:
session.add(new_record)
# 提交即保存到数据库:
session.commit()
print new_record.id


# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
task_record = session.query(task_record).filter(task_record.id==new_record.id).one()
# 打印类型和对象的name属性:
print 'command:', task_record.command
print 'success:', task_record.success
print 'error:', task_record.error
# 关闭Session:
session.close()