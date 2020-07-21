#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : ${DATE} ${HOUR}:${MINUTE}
# @Author  : wuweizeng
# @Email   : tielemao@163.com
# @Site    : ${SITE}
# @File    : ${NAME}.py
# @Software: ${PRODUCT_NAME}

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler

# 注册APScheduler
scheduler = APScheduler()

# 每天的北京时间9：00分触发一次下载邮件并判断和自动导入googsheets的任务
@scheduler.task('cron', id='do_job_1', hour=8, minute=30, day_of_week='0-6')
def job1():
    email_attach.main()

@scheduler.task('cron', id='do_job_2', hour=9, minute=0, day_of_week='0-6')
def job2():
    result = week_task()
    if type(result) == dict:
        data = models.Analyze(result=result)
        db.session.add(data)
        db.session.commit()

@scheduler.task('cron', id='do_job_3', hour=9, minute=15, day_of_week='0-6')
def job3():
    result = month_task()
    if type(result) == dict:
        data = models.Analyze(result=result)
        db.session.add(data)
        db.session.commit()

app = Flask(__name__)
app.config.from_object(Config)
# 防止定时任务重复执行两次
app.debug = False
app.use_reloader = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bookstrap = Bootstrap(app)
from collect import routes, models
import email_attach
from hr2google import week_task, month_task
scheduler.init_app(app)
scheduler.start()

