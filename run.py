#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 六  2/11 16:39:14 2017
# @Description:
import sys
from fabric.api import run, env

env.host_string = 'localhost';
run('pwd')
print sys.stdout
