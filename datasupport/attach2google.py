#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/13 16:45
# @Update  : 2019/11/13 16:45
# @Author  : wuweizeng
# @Email   : tielemao@163.com
# @File    : attach2google.py
# @Desc    : 扫描附件，符合条件的自动处理导入到googlesheets

import os
import time, datetime
from google_sheets2 import GoogleSheets


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


def update(filename, file2_name):
    """
    采集和更新数据到 googsheets 上的 DataSource
    :param kwargs:
    :return:
    """
    tables_name = "IT数据支持系统"
    sheet_name = "DataSource_1.0"
    hr_googlesheets = GoogleSheets(filename=filename, file2_name=file2_name, tables_name=tables_name,
                                   sheet_name=sheet_name)
    return hr_googlesheets.append()


def main():
    basedir = os.path.abspath(os.path.dirname(__file__))
    upload_folder = os.path.join(basedir, 'static/uploads')
    file_list = ["《招聘数据统计表》.xlsx", "《阶段通过情况》.xlsx"]
    file_path = []
    for name in file_list:
        filepath = os.path.join(upload_folder, name)
        file_path.append(filepath)
    # 如果扫描到满足条件,则自动导入数据到googsheets上面
    if scan_attach(file_path=file_path):
        return update(filename="《招聘数据统计表》.xlsx", file2_name="《阶段通过情况》.xlsx")


if __name__ == '__main__':
    main()
