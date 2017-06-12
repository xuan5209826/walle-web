#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

from sqlalchemy import Column, String, Integer, create_engine, Text, DateTime, desc, or_

from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from pickle import dump

# from flask_cache import Cache
from datetime import datetime

from walle.database import Column, SurrogatePK, db, reference_col, relationship

from walle.database import Model
from sqlalchemy.orm import aliased
import logging


# 上线单
class Task(SurrogatePK, Model):
    __tablename__ = 'task'
    current_time = datetime.now()

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(100))
    user_id = db.Column(Integer)
    project_id = db.Column(Integer)
    action = db.Column(Integer)
    status = db.Column(Integer)
    link_id = db.Column(String(100))
    ex_link_id = db.Column(String(100))
    servers = db.Column(Text)
    commit_id = db.Column(String(40))
    branch = db.Column(String(100))
    file_transmission_mode = db.Column(Integer)
    file_list = db.Column(Text)
    enable_rollback = db.Column(Integer)
    created_at = db.Column(DateTime, default=current_time)
    updated_at = db.Column(DateTime, default=current_time, onupdate=current_time)

    taskMdl = None

    def table_name(self):
        return self.__tablename__

    #
    # def list(self, page=0, size=10, kw=''):
    #     data = Task.query.order_by('id').offset(int(size) * int(page)).limit(size).all()
    #     return [p.to_json() for p in data]
    #
    # def one(self):
    #     project_info = Project.query.filter_by(id=self.taskMdl.get('project_id')).one().to_json()
    #     return dict(project_info, **self.taskMdl)
    #

    def list(self, page=0, size=10, kw=None):
        """
        获取分页列表
        :param page:
        :param size:
        :param kw:
        :return:
        """
        query = Task.query
        if kw:
            query = query.filter(Task.name.like('%' + kw + '%'))
        count = query.count()

        data = query.order_by('id desc') \
            .offset(int(size) * int(page)).limit(size) \
            .all()
        task_list = []

        for task in data:
            task = task.to_json()
            project = Project().get_by_id(task['project_id']).to_dict()
            task['project_name'] = project['name'] if project else u'未知项目'
            task_list.append(task)

        return task_list, count

    def item(self, id=None):
        """
        获取单条记录
        :param role_id:
        :return:
        """
        id = id if id else self.id
        data = self.query.filter_by(id=id).first()
        if not data:
            return []

        task = data.to_json()
        project = Project().get_by_id(task['project_id']).to_dict()
        task['project_name'] = project['name'] if project else u'未知项目'
        return task

    def add(self, *args, **kwargs):
        # todo permission_ids need to be formated and checked
        data = dict(*args)
        f = open('run.log', 'w')
        f.write('\n====add===\n' + str(data))
        project = Task(**data)

        db.session.add(project)
        db.session.commit()

        if project.id:
            self.id = project.id

        return project.id

    def update(self, *args, **kwargs):
        # todo permission_ids need to be formated and checked
        # a new type to update a model

        update_data = dict(*args)
        return super(Task, self).update(**update_data)

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
            'user_id': int(self.user_id),
            'project_id': int(self.project_id),
            'action': self.action,
            'status': self.status,
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
    status_close = 2
    current_time = datetime.now()

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(20))
    status = db.Column(Integer)
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
            query = query.filter(Environment.name.like('%' + kw + '%'))
        count = query.count()

        data = query.order_by('id desc').offset(int(size) * int(page)).limit(size).all()
        env_list = [p.to_json() for p in data]
        return env_list, count

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
        db.session.commit()
        if env.id:
            self.id = env.id

        return env.id

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
            'env_name': self.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


# server
class Server(SurrogatePK, Model):
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
            query = query.filter(Server.name.like('%' + kw + '%'))
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
        server = Server(name=name, host=host)

        db.session.add(server)
        db.session.commit()
        if server.id:
            self.id = server.id

        return server.id

    def update(self, name, host, id=None):
        # todo permission_ids need to be formated and checked
        id = id if id else self.id
        role = Server.query.filter_by(id=id).first()

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


# 项目配置表
class Project(SurrogatePK, Model):
    # 表的名字:
    __tablename__ = 'project'
    current_time = datetime.now()
    status_close = 0
    status_open = 1

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
    server_ids = db.Column(Text)
    task_vars = db.Column(Text)
    prev_deploy = db.Column(Text)
    post_deploy = db.Column(Text)
    prev_release = db.Column(Text)
    post_release = db.Column(Text)
    keep_version_num = db.Column(Integer)
    repo_url = db.Column(String(200))
    repo_username = db.Column(String(50))
    repo_password = db.Column(String(50))
    repo_mode = db.Column(String(50))
    repo_type = db.Column(String(10))

    created_at = db.Column(DateTime, default=current_time)
    updated_at = db.Column(DateTime, default=current_time, onupdate=current_time)

    def list(self, page=0, size=10, kw=None):
        """
        获取分页列表
        :param page:
        :param size:
        :return:
        """
        query = self.query
        if kw:
            query = query.filter(Project.name.like('%' + kw + '%'))
        count = query.count()
        data = query.order_by('id desc').offset(int(size) * int(page)).limit(size).all()
        list = [p.to_json() for p in data]
        return list, count

    def item(self, id=None):
        """
        获取单条记录
        :param role_id:
        :return:
        """
        id = id if id else self.id
        data = self.query.filter_by(id=id).first()

        if not data:
            return []

        data = data.to_json()

        server_ids = data['server_ids']
        # return map(int, server_ids.split(','))
        # with_entities('name')
        servers = Server().query.filter(Server.id.in_(map(int, server_ids.split(',')))).all()
        servers_info = []
        for server in servers:
            servers_info.append({
                'id': server.id,
                'name': server.name,
            })
        data['server_ids'] = servers_info
        return data

    def add(self, *args, **kwargs):
        # todo permission_ids need to be formated and checked
        data = dict(*args)
        f = open('run.log', 'w')
        f.write(str(data))
        project = Project(**data)

        db.session.add(project)
        db.session.commit()
        self.id = project.id
        return self.id

    def update(self, *args, **kwargs):
        # todo permission_ids need to be formated and checked
        # a new type to update a model

        update_data = dict(*args)
        return super(Project, self).update(**update_data)

    def remove(self, role_id=None):
        """

        :param role_id:
        :return:
        """
        role_id = role_id if role_id else self.id
        Project.query.filter_by(id=role_id).delete()
        return db.session.commit()

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
            'server_ids': self.server_ids,
            'task_vars': self.task_vars,
            'prev_deploy': self.prev_deploy,
            'post_deploy': self.post_deploy,
            'prev_release': self.prev_release,
            'post_release': self.post_release,
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
class User(UserMixin, SurrogatePK, Model):
    # 表的名字:
    __tablename__ = 'user'

    current_time = datetime.now()
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

    def set_password(self, password):
        """Set password."""
        self.password = generate_password_hash(password)

    def general_password(self, password):
        """
        检查密码是否正确
        :param password:
        :return:
        """
        self.password = generate_password_hash(password)
        return generate_password_hash(password)

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
        count = query.count()
        data = query.order_by('id desc').offset(int(size) * int(page)).limit(size).all()
        user_list = [p.to_json() for p in data]
        return user_list, count

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


class Access(db.Model):
    __tablename__ = 'access'

    type_module = 'module'
    type_controller = 'controller'
    type_action = 'action'

    status_open = 1
    status_close = 2
    current_time = datetime.now()

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name_cn = db.Column(String(30))
    name_en = db.Column(String(30))
    pid = db.Column(Integer)
    type = db.Column(String(30))
    sequence = db.Column(Integer)
    archive = db.Column(Integer)
    icon = db.Column(String(30))
    fe_url = db.Column(String(30))
    fe_visible = db.Column(Integer)
    created_at = db.Column(DateTime, default=current_time)
    updated_at = db.Column(DateTime, default=current_time, onupdate=current_time)

    def menu(self, role):
        role_id = 1
        role = Role(id=role_id).item()
        data = {}

        query = self.query.filter_by(fe_visible=1) \
            .filter(Access.type.in_((self.type_module, self.type_controller))) \
            .filter(Access.id.in_(role['access_ids'].split(','))) \
            .order_by('sequence asc') \
            .all()
        for item in query:
            logging.error(str(item.to_json()))
            if item.type == self.type_module:
                data[item.id] = {
                    'title': item.name_cn,
                    'icon': item.icon,
                }
            elif item.type == self.type_controller:
                if not data[item.pid].has_key('sub_menu'):
                    data[item.pid]['sub_menu'] = []
                data[item.pid]['sub_menu'].append({
                    'title': item.name_cn,
                    'icon': item.icon,
                    'fe_url': item.fe_url,
                })

        return data.values()

    def list(self):
        """
        获取分页列表
        :param page:
        :param size:
        :param kw:
        :return:
        """
        menus_module = {}
        menus_controller = {}
        module = aliased(Access)
        controller = aliased(Access)
        action = aliased(Access)

        data = db.session.query(module.id, module.name_cn, controller.id, controller.name_cn, action.id, action.name_cn)\
            .outerjoin(controller, controller.pid==module.id)\
            .outerjoin(action, action.pid==controller.id)\
            .filter(module.type==self.type_module)\
            .all()
        for m_id, m_name, c_id, c_name, a_id, a_name in data:
            # module
            if not menus_module.has_key(m_id):
                menus_module[m_id] = {
                    'id': m_id,
                    'title': m_name,
                    'sub_menu': {},
                }
            # controller
            if not menus_module[m_id]['sub_menu'].has_key(c_id) and c_name:
                menus_module[m_id]['sub_menu'][c_id] = {
                    'id': c_id,
                    'title': c_name,
                    'sub_menu': {},
                }
            # action
            if not menus_controller.has_key(c_id):
                menus_controller[c_id] = []
            if a_name:
                menus_controller[c_id].append({
                    'id': a_id,
                    'title': a_name,
                })
        menus = []
        logging.error(type(menus_module))
        for m_id, m_info in menus_module.items():
            for c_id, c_info in m_info['sub_menu'].items():
                m_info['sub_menu'][c_id]['sub_menu'] = menus_controller[c_id]
            menus.append({
                'title': m_info['title'],
                'sub_menu': m_info['sub_menu'].values(),
            })

        return menus

    def to_json(self):
        return {
            'id': self.id,
            'name_cn': self.name_cn,
            'name_en': self.name_en,
            'pid': self.pid,
            'type': self.type,
            'sequence': self.sequence,
            'archive': self.archive,
            'icon': self.icon,
            'fe_url': self.fe_url,
            'fe_visible': self.fe_visible,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


# 项目配置表
class Role(UserMixin, SurrogatePK, Model):
    # 表的名字:
    __tablename__ = 'role'

    # current_time = datetime.now()
    current_time = datetime.now()

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(30))
    access_ids = db.Column(Text, default='')
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
        data = Role.query.filter_by(id=role_id).first()
        return data.to_json() if data else []

    def add(self, name, access_ids):
        # todo access_ids need to be formated and checked
        role = Role(name=name, access_ids=access_ids)

        db.session.add(role)
        db.session.commit()
        self.id = role.id
        return self.id

    def update(self, name, access_ids, role_id=None):
        # todo access_ids need to be formated and checked
        role_id = role_id if role_id else self.id
        role = Role.query.filter_by(id=role_id).first()
        role.name = name
        role.access_ids = access_ids

        return db.session.commit()

    def remove(self, role_id=None):
        """

        :param role_id:
        :return:
        """
        role_id = role_id if role_id else self.id
        Role.query.filter_by(id=role_id).delete()
        return db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'role_name': self.name,
            'access_ids': self.access_ids,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


# 项目配置表
class Tag(SurrogatePK, Model):
    # 表的名字:
    __tablename__ = 'tag'

    current_time = datetime.now()

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(30))
    label = db.Column(String(30))
    # users = db.relationship('Group', backref='group', lazy='dynamic')
    created_at = db.Column(DateTime, default=current_time)
    updated_at = db.Column(DateTime, default=current_time, onupdate=current_time)

    def list(self):
        data = Tag.query.filter_by(id=1).first()
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
        # user_ids = []
        # for user in self.users.all():
        #     user_ids.append(user.user_id)
        return {
            'id': self.id,
            'group_id': self.id,
            'group_name': self.name,
            # 'users': user_ids,
            # 'user_ids': user_ids,
            'label': self.label,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


# 项目配置表
class Group(SurrogatePK, Model):
    __tablename__ = 'user_group'

    current_time = datetime.now()

    # 表的结构:
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, db.ForeignKey('user.id'))
    user_ids = db.relationship('Tag', backref=db.backref('users'))
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
        group = Group.query
        if kw:
            group = group.filter_by(Tag.name.like('%' + kw + '%'))
        group = group.offset(int(size) * int(page)).limit(size).all()
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

        query = Tag.query
        if kw:
            query = query.filter(Tag.name.like('%' + kw + '%'))
        count = query.count()
        data = query.order_by('id desc').offset(int(size) * int(page)).limit(size).all()
        list = [p.to_json() for p in data]
        return list, count

    def add(self, group_name, user_ids):
        tag = Tag(name=group_name, label='user_group')
        db.session.add(tag)
        db.session.commit()

        for user_id in user_ids:
            user_group = Group(group_id=tag.id, user_id=user_id)
            db.session.add(user_group)

        db.session.commit()
        if tag.id:
            self.group_id = tag.id

        return tag.id

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

    def item(self, group_id=None):
        """
        获取单条记录
        :param role_id:
        :return:
        """
        #
        group_id = group_id if group_id else self.group_id
        tag = Tag.query.filter_by(id=group_id).first()
        if not tag:
            return None
        tag = tag.to_json()

        group_id = group_id if group_id else self.group_id
        groups = Group.query.filter_by(group_id=group_id).all()

        user_ids = []
        for group_info in groups:
            user_ids.append(group_info.user_id)

        tag['user_ids'] = user_ids
        tag['users'] = len(user_ids)
        return tag

        del group_dict['user_id']
        # return user_ids
        return group_dict
        return group.to_json()
        # group = group.to_json()

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
