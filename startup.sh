#!/usr/bin/env zsh
###################################################################
# @Author: wushuiyong
# @Created Time : 三  1/ 4 23:07:56 2017
#
# @File Name: cel_start.sh
# @Description:
###################################################################

# websocket 启动
python ws.py

# redis 启动
redis-server

# celery 启动
celery -A cel worker --loglevel=info
