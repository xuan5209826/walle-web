#!/usr/bin/env zsh
###################################################################
# @Author: wushuiyong
# @Created Time : 二  5/23 23:06:06 2017
#
# @File Name: run.sh
# @Description:
###################################################################
source venv/bin/activate
export FLASK_APP=autoapp.py
export FLASK_DEBUG=1
python -m flask run
