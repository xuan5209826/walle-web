#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 一  1/ 2 19:08:16 2017
# @Description:

import datetime
import json

date = str(datetime.datetime.now())
print json.dumps({
    "time" : date
})
