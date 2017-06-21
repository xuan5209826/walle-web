#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

import logging
from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import aliased

from walle.model.database import db
from walle.model.role import RoleModel


class AccessModel(db.Model):
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
        role = RoleModel(id=role_id).item()
        data = {}

        query = self.query.filter_by(fe_visible=1) \
            .filter(AccessModel.type.in_((self.type_module, self.type_controller))) \
            .filter(AccessModel.id.in_(role['access_ids'].split(','))) \
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
        module = aliased(AccessModel)
        controller = aliased(AccessModel)
        action = aliased(AccessModel)

        data = db.session.query(module.id, module.name_cn, controller.id, controller.name_cn, action.id, action.name_cn) \
            .outerjoin(controller, controller.pid == module.id) \
            .outerjoin(action, action.pid == controller.id) \
            .filter(module.type == self.type_module) \
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
                'id': m_id,
                'title': m_info['title'],
                'sub_menu': m_info['sub_menu'].values(),
            })

        return menus

    def fetch_access_list_by_role_id(self, role_id):
        module = aliased(Access)
        controller = aliased(Access)
        action = aliased(Access)
        role = RoleModel.query.get(role_id)
        access_ids = role.access_ids.split(',')

        data = db.session \
            .query(controller.name_en, controller.name_cn,
                   action.name_cn, action.name_cn) \
            .outerjoin(action, action.pid == controller.id) \
            .filter(module.type == self.type_module) \
            .filter(controller.id.in_(access_ids)) \
            .filter(action.id.in_(access_ids)) \
            .all()
        return []
        # return [rbac.AccessModel.resource(a_en, c_en) for c_en, c_cn, a_en, a_cn in data if c_en and a_en]

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
