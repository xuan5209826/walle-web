#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:
import model

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def save_record(stage, sequence, user_id, task_id, status, command, success, error):

    # 初始化数据库连接:
    engine = create_engine('mysql://root:whoiam@localhost:3306/walle-python')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    # 创建Session:
    session = DBSession()

    # 创建新User对象:
    new_record = model.task_record(
        stage=stage,
        sequence=sequence,
        user_id=user_id,
        task_id=task_id,
        status=status,
        command=command,
        success=success,
        error=error,
    )
    # 添加到session:
    session.add(new_record)
    # 提交即保存到数据库:
    session.commit()
    print new_record.id


    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    task_record = session.query(model.task_record).filter(model.task_record.id==new_record.id).one()
    # 打印类型和对象的name属性:
    print 'command:', task_record.command
    print 'success:', task_record.success
    print 'error:', task_record.error
    # 关闭Session:
    session.close()