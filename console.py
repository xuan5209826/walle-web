#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import os
from StringIO import StringIO

import cel
import os, datetime
from fabric.api import run, env, local, cd, execute, sudo
from fabric import context_managers, colors
import subprocess
#variable 'out' is subprocess output info
top_info = subprocess.Popen(["top", "-n", "1"], stdout=subprocess.PIPE)
out, err = top_info.communicate()

#output info get from console has many unicode escape character ,such as \x1b(B\x1b[m\x1b[39;49m\x1b[K\n\x1b(B\x1b[m
#use decode('unicode-escape') to process

out_info = out.decode('unicode-escape')
print(out_info)

lines = []
lines = out_info.split('\n')
print lines