# -*- coding: utf-8 -*-
"""
    walle-web

    :copyright: © 2015-2017 walle-web.io
    :created time: 2017-06-14 15:53:46
    :author: wushuiyong@walle-web.io
"""

import logging

from walle.extensions import login_manager
from walle.model import models


@login_manager.user_loader
def load_user(user_id):
    logging.error(user_id)
    user = models.User.query.get(user_id)
    role = models.Role().item(user.role_id)
    access = models.Access().fetch_access_list_by_role_id(user.role_id)
    logging.error(access)
    # logging.error(models.Role.query.get(user.role_id).access_ids)
    # logging.error(role['access_ids'].split(','))
    # logging.error(models.User.query.get(user_id))
    return models.User.query.get(user_id)
