#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2019/11/19 16:58
# @Update  : 2019/11/19 16:58
# @Author  : wuweizeng
# @Email   : tielemao@163.com
# @File    : hr_data.py
# @Desc    : 采集HR数据写入谷歌sheets相应表上的周报和月报

import os
import time
import datetime
import pygsheets
import pandas as pd
import ReportValues
from xlsx2csv import Xlsx2csv

basedir = os.path.abspath(os.path.dirname(__file__))
auth_path = os.path.join(basedir, 'auth/ItSupport.json')
upload_folder = os.path.join(basedir, 'static/uploads')
log_path = os.path.join(basedir, 'log')


class HrGoogleSheets(object):

    def __init__(self, tables_name="IT数据支持系统"):
        """
        :param filename: 周报表格
        :param tables_name: 表格名，默认"IT数据支持系统"
        :param sheet_name: 表格页名，默认为"data-weekly", 月报是"data-monthly"
        """
        # authorization OAuth2.0
        self.gc = pygsheets.authorize(client_secret=auth_path)
        # open the google spreadsheet
        self.sh = self.gc.open(tables_name)

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

    def append_weekly(self, filename, sheet_name="data-weekly"):
        """
        追加一行数据到周报表格的最后一行
        :return:
        """
        try:
            # select the sheet for sheet name
            wks = self.sh.worksheet_by_title(title=sheet_name)
            file_path1 = os.path.join(upload_folder, self.xlsx_to_csv(filename))
            # 获取一个包含所有采集和处理过的值的字典
            hr_report = ReportValues.ReportPass(srcd=file_path1)
            statistics = hr_report.GetWeekData()
            # today = str(datetime.date.today())
            today = time.strftime("%Y-%m-%d %H:%M:%S")
            table_values = [today, statistics["简历数"], statistics["推荐简历数"], statistics["推荐简历通过数"], \
                            statistics["专业面试数"], statistics["综合面试数"], statistics["创建offer数"], \
                            statistics["入职人数"],
                            ]
            wks.append_table(table_values)
            return statistics
        except Exception as e:
            # 将错误写入日志，方便判断是哪一步出错
            error_log = os.path.join(log_path, str(datetime.date.today()) + '_error.log')
            with open(error_log, 'a') as f:
                f.write(str(e))
            return e

    def append_monthly(self, filename, filename2, sheet_name="data-monthly"):
        """
        追加一行数据到月报表格的最后一行
        :return:
        """
        try:
            # select the sheet for sheet name
            wks = self.sh.worksheet_by_title(title=sheet_name)
            file_path1 = os.path.join(upload_folder, self.xlsx_to_csv(filename))
            file_path2 = os.path.join(upload_folder, self.xlsx_to_csv(filename2))
            # 获取一个包含所有采集和处理过的值的字典
            hr_report = ReportValues.ReportPass(srcd=file_path1, srcc=file_path2)
            statistics = hr_report.GetMonData()
            # today = str(datetime.date.today())
            today = time.strftime("%Y-%m-%d %H:%M:%S")
            table_values = [today, statistics["初试数"], statistics["复试数"], statistics["创建offer数"], \
                            statistics["入职人数"], statistics["职位数"], statistics["合格简历倍数"], \
                            statistics["简历等级A"], statistics["简历等级A+"], statistics["简历等级S"], \
                            statistics["岗位成功关闭率"], statistics["初筛通过率"], statistics["用人部门筛选通过率"], \
                            statistics["初试通过率"], statistics["复试通过率"], statistics["外部招聘OFFER接受率"], \
                            statistics["入职率"], statistics["初筛周期"], statistics["用人部门筛选周期"], \
                            statistics["面试周期"], statistics["offer发放周期"], statistics["待入职周期"],
                            ]
            wks.append_table(table_values)
            return statistics
        except Exception as e:
            # 将错误写入日志，方便判断是哪一步出错
            error_log = os.path.join(log_path, str(datetime.date.today()) + '_error.log')
            with open(error_log, 'a') as f:
                f.write(str(e))
            return e
