# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
from datetime import datetime
import time


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def date_str_to_obj(ymd):
    return time.strptime(ymd, '%Y-%m-%d')


def datetime_str_to_obj(ymd_his):
    return datetime.strptime(ymd_his, "%Y-%m-%d %H:%i:%s")
