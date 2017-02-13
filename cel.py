#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

from celery import Celery
import os
from fabric.api import *
import waller
from waller import *

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')

@app.task
def add(command):
    out_file = '/tmp/ws_01'
    cmd = '%s > %s' % (command, out_file)
    done = os.system(cmd)
    stdOut = open(out_file)
    output = stdOut.read()
    print output
    return output

@app.task
def prev_deploy(SocketHandler):
    walle = waller()
    walle.prev_deploy(SocketHandler)
