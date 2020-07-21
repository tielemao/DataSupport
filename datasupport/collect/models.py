#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Update  : 2019-11-15
# @Author  : wuweizeng
# @Email   : tielemao@163.com
# @File    : models.py
# @Desc    : 数据库

import datetime
from collect import db
from collect import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index, JSON


class User(UserMixin, db.Model):
    """
    用户表
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

class Analyze(db.Model):
    """
    分析表，用于保存每次去获取的分析json结果
    """
    __tablename__ = 'analyze'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.now)
    result = Column(JSON, nullable=True)
