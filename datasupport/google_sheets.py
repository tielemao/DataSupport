#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/4 17:14
# @Update  : 2019/11/7
# @Author  : wuweizeng
# @Email   : tielemao@163.com
# @File    : google_sheets.py
# @Desc    : 收集和处理数据后填入googlesheets

import os.path
from collect import app
import pygsheets
import pandas as pd
from ReportValues_old import StagePass
from xlsx2csv import Xlsx2csv

basedir = os.path.abspath(os.path.dirname(__file__))
auth_path = os.path.join(basedir, 'auth/ItSupport.json')

class GoogleSheets:

    def __init__(self, filename, file2_name, tables_name, sheet_num):
        """
        :param filename: 文件名，纯英文
        :param tables_name: 表格名，默认"IT数据系统"
        :param sheet_num: 表格页索引，默认0，第一页
        """
        # authorization OAuth2.0
        self.gc = pygsheets.authorize(client_secret=auth_path)
        # open the google spreadsheet
        self.sh = self.gc.open(tables_name)
        # select the sheet
        self.wks = self.sh[int(sheet_num)]
        self.filename = filename
        self.file2_name = file2_name

    def xlsx_to_csv(self, file_names):
        """
        传入xlsx文件名,存为csv文件, 同时返回csv扩展名的文件名
        :return:
        """
        file_name = file_names.split('.')[0]  # 获取不带扩展名的文件名
        xlsx_path = os.path.join(app.config['UPLOAD_FOLDER'], file_names)
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name + '.csv')
        Xlsx2csv(xlsx_path, outputencoding="utf-8").convert(csv_path)
        return file_name + '.csv'

    def update(self):
        try:
            file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], self.xlsx_to_csv(self.filename))
            file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], self.xlsx_to_csv(self.file2_name))
            # 获取一个包含所有采集和处理过的值的字典
            hr_report = StagePass(srcd=file_path1, srcc=file_path2)
            statistics = hr_report.GetDict()
            self.wks.update_value("K7", statistics["招聘违规率"][0])
            self.wks.update_value("L9", statistics["职位数"][0])
            self.wks.update_value("L10", statistics["初筛数"][0])
            self.wks.update_value("L11", statistics["初筛平均处理周期"][0])
            self.wks.update_value("J12", statistics["初筛通过率"][0])
            self.wks.update_value("K12", statistics["初筛通过率"][1])
            self.wks.update_value("L13", statistics["推荐简历数"][0])
            self.wks.update_value("L14", statistics["推荐简历等级比例"][0])
            self.wks.update_value("L15", statistics["简历推荐通过数"][0])
            self.wks.update_value("J16", statistics["简历推荐通过率"][0])
            self.wks.update_value("K16", statistics["简历推荐通过率"][1])
            self.wks.update_value("L17", statistics["用人部门筛选简历平均处理周期"][0])
            self.wks.update_value("J18", statistics["合格简历倍数"][0])
            self.wks.update_value("K18", statistics["合格简历倍数"][1])
            self.wks.update_value("L19", statistics["安排面试数"][0])
            self.wks.update_value("J20", statistics["邀约成功率"][0])
            self.wks.update_value("K20", statistics["邀约成功率"][1])
            self.wks.update_value("K21", statistics["面试通过率"][0])
            self.wks.update_value("L22", statistics["面试平均处理周期"][0])
            self.wks.update_value("L25", statistics["沟通offer平均处理周期"][0])
            self.wks.update_value("J26", statistics["外部招聘OFFER接受率"][0])
            self.wks.update_value("K26", statistics["外部招聘OFFER接受率"][1])
            self.wks.update_value("J27", statistics["人均创建offer的申请数"][0])
            self.wks.update_value("J28", statistics["外部招聘平均到岗时间"][0])
            self.wks.update_value("K28", statistics["外部招聘平均到岗时间"][1])
            self.wks.update_value("J29", statistics["岗位成功关闭率"][0])
            self.wks.update_value("K29", statistics["岗位成功关闭率"][1])
            return statistics
        except Exception as e:
            return e

