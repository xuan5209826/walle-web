#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:
from celery import Celery
import os

app = Celery('tasks', broker='redis://localhost')

@app.task
def add(command):
    out_file = '/tmp/ws_01'
    cmd = '%s > %s' % (command, out_file)
    done = os.system(cmd)
    stdOut = open(out_file)
    output = stdOut.read()
    print output
    return output