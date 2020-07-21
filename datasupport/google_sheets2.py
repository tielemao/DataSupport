#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/14
# @Update  : 2019/11/15
# @Author  : wuweizeng
# @Email   : tielemao@163.com
# @File    : google_sheets.py
# @Desc    : 收集和处理数据后填入googlesheets

import os
import time
import datetime
import pygsheets
import pandas as pd
from ReportValues_old import StagePass
from xlsx2csv import Xlsx2csv

basedir = os.path.abspath(os.path.dirname(__file__))
auth_path = os.path.join(basedir, 'auth/ItSupport.json')
upload_folder = os.path.join(basedir, 'static/uploads')
log_path = os.path.join(basedir, 'log')


class GoogleSheets(object):

    def __init__(self, filename, file2_name, tables_name="IT数据支持系统", sheet_name="DataSource_1.0"):
        """
        :param filename: 第一张表格
        :param file2_name: 第二张表格
        :param tables_name: 表格名，默认"IT数据支持系统"
        :param sheet_name: 表格页名，默认为DataSource_1.0
        """
        # authorization OAuth2.0
        self.gc = pygsheets.authorize(client_secret=auth_path)
        # open the google spreadsheet
        self.sh = self.gc.open(tables_name)
        # select the sheet for sheet name
        self.wks = self.sh.worksheet_by_title(title=sheet_name)
        self.filename = filename
        self.file2_name = file2_name

    def xlsx_to_csv(self, file_names):
        """
        传入xlsx文件名,存为csv文件, 同时返回csv扩展名的文件名
        :return:
        """
        file_name = file_names.split('.')[0]  # 获取不带扩展名的文件名
        xlsx_path = os.path.join(upload_folder, file_names)
        csv_path = os.path.join(upload_folder, file_name + '.csv')
        Xlsx2csv(xlsx_path, outputencoding="utf-8").convert(csv_path)
        return file_name + '.csv'


    def append(self):
        """
        追加一行数据到表格的最后一行
        :return:
        """
        try:
            file_path1 = os.path.join(upload_folder, self.xlsx_to_csv(self.filename))
            file_path2 = os.path.join(upload_folder, self.xlsx_to_csv(self.file2_name))
            # 获取一个包含所有采集和处理过的值的字典
            hr_report = StagePass(srcd=file_path1, srcc=file_path2)
            statistics = hr_report.GetDict()
            # today = str(datetime.date.today())
            today = time.strftime("%Y-%m-%d %H:%M:%S")
            ratio = statistics["推荐简历等级比例"][-1].split(":")
            table_values = [today, statistics["初筛数"][-1], statistics["推荐简历数"][-1], \
                            statistics["简历推荐通过数"][-1], statistics["安排面试数"][0], '-', \
                            '-', statistics["创建offer数"][-1], statistics["职位数"][-1], \
                            statistics["合格简历倍数"][-1], ratio[0], ratio[1], ratio[2], \
                            statistics["初筛通过率"][-1], statistics["简历推荐通过率"][-1], \
                            statistics["邀约成功率"][-1], '-', '-', '-', '-', \
                            statistics["外部招聘OFFER接受率"][-1], statistics["岗位成功关闭率"][-1], \
                            statistics["初筛平均处理周期"][-1], statistics["用人部门筛选简历平均处理周期"][-1], \
                            statistics["面试平均处理周期"][-1], statistics["沟通offer平均处理周期"][-1], \
                            statistics["外部招聘平均到岗时间"][-1], '-', '-', '-', '-', '-', '-', '-',
                            ]
            self.wks.append_table(table_values)
            return statistics
        except Exception as e:
            # 将错误写入日志，方便判断是哪一步出错
            error_log = os.path.join(log_path, str(datetime.date.today()) + '_error.log')
            with open(error_log, 'a') as f:
                f.write(e)
            return e
