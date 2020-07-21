#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/20 17:21
# @Update  : 2019/11/20 17:21
# @Author  : wuweizeng
# @Email   : tielemao@163.com
# @File    : hr2google.py
# @Desc    : 扫描附件，HR部门符合条件的自动处理导入到googlesheets

import os
import time, datetime
from hr_data import HrGoogleSheets

basedir = os.path.abspath(os.path.dirname(__file__))
upload_folder = os.path.join(basedir, 'static/uploads')

def scan_attach(file_path):
    """
    进行扫描附件目录，判断有没有存在最新的表格文件
    :return:
    """
    today = datetime.date.today()
    for path in file_path:
        try:
            file_ctime = time.ctime(os.stat(path).st_ctime)  # 文件创建时间
            file_datetime = datetime.datetime.strptime(file_ctime, "%a %b %d %H:%M:%S %Y")  # 转换为datetime格式
            file_date = file_datetime.date()
            diff = today - file_date
            # 如果今天的时间大于文件创建的时间
            if diff.days != 0:
                # 不满足触发导入
                return
        except IOError:
            return
    return True


def append_week(filename):
    """
    采集和更新周报数据到 googsheets 上的 data-weekly
    :param kwargs:
    :return:
    """
    tables_name = "IT数据支持系统"
    sheet_name = "data-weekly"
    hr_week = HrGoogleSheets()
    result = hr_week.append_weekly(filename, sheet_name=sheet_name)
    return result


def append_month(filename,filename2):
    """
    采集和更新月报数据到 googsheets 上的 data-monthly
    :param kwargs:
    :return:
    """
    tables_name = "IT数据支持系统"
    sheet_name = "data-monthly"
    hr_month = HrGoogleSheets()
    result = hr_month.append_monthly(filename, filename2, sheet_name=sheet_name)
    return result


def week_task():
    """
    执行周报的定时任务
    :return:
    """
    file_list = ["《周招聘数据统计表》.xlsx", ]
    file_path = []
    for name in file_list:
        filepath = os.path.join(upload_folder, name)
        file_path.append(filepath)
    # 如果扫描到满足条件,则自动导入数据到googsheets上面
    if scan_attach(file_path=file_path):
        result = append_week(filename="《周招聘数据统计表》.xlsx")
    return result


def month_task():
    """
    执行月报的定时任务
    :return:
    """
    file_list = ["《月招聘数据统计表》.xlsx", "《月阶段通过情况》.xlsx"]
    file_path = []
    for name in file_list:
        filepath = os.path.join(upload_folder, name)
        file_path.append(filepath)
    # 如果扫描到满足条件,则自动导入数据到googsheets上面
    if scan_attach(file_path=file_path):
        result = append_month(filename="《月招聘数据统计表》.xlsx", filename2="《月阶段通过情况》.xlsx")
    return result



