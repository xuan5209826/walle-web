#!/usr/bin/env zsh
###################################################################
# @Author: wushuiyong
# @Created Time : 三  1/ 4 23:07:56 2017
#
# @File Name: cel_start.sh
# @Description:
###################################################################
 celery -A cel worker --loglevel=info
