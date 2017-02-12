#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong@walle-web.io
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

from cel import add

add.delay('echo pwd && pwd && sleep 3 && echo ls && ls')
