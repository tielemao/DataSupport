#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-10-30
# @Author  : wuweizeng
# @Email   : tielemao@163.com
# @File    : hr.py

from collect import app, db
from collect.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
