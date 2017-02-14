#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 六  2/11 16:39:14 2017
# @Description:
import sys
from sql import save_record
from fabric.api import run, env

command='pwd'
env.host_string = 'localhost';
run(command)

save_record(stage='prev', sequence=9, user_id=33, task_id=32, status=1, command=command, success='/User/wushuiyong', error='');