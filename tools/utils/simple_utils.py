#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-11-13 16:06
import os
from uuid import uuid4 as uuid
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


def get_file_names(file_dir, file_type):
    """
    得到某个目录下所有的文件名
    :param file_dir:文件夹路径
    :param file_type:后缀名
    :return:
    """
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == "." + file_type:
                # L.append(os.path.join(root, file))
                L.append(os.path.join(file))
    return L


def get_folder_names(file_dir):
    """
    得到某个目录下所有的文件夹名
    :param file_dir:文件夹路径
    :return:
    """
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in dirs:
            L.append(os.path.join(file))
    return L


def get_file_names_without_type(file_dir):
    """
    得到某个目录下所有的文件名
    :param file_dir:文件夹路径
    :return:
    """
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            L.append(os.path.join(file))
    return L


def get_uuid():
    """
    获取一个uuid，去除了'-'
    :return:
    """
    return str(uuid()).replace("-", "")


def file_extension(path):
    """
    获取一个文件路径的扩展名  .txt
    :param path:
    :return:
    """
    return os.path.splitext(path)[1]


# from pydocx import PyDocX
# import requests
# def doc2docx(file_path):
#     '''
#     将doc使用unoconv服务转换成docx
#     :param file_path:
#     :return:
#     '''
#     # 如果是，通过unoconv进行转换
#     response = requests.post("http://" + conf.unoconv_host + ":3000/unoconv/docx",
#                              files={'file': open(file_path, 'rb')})
#     return response.content

# def docx2html(file_path):
#     '''
#     将一个docx转换成html
#     :param file_path:
#     :return:
#     '''
#     return PyDocX.to_html(file_path)

def get_file_name_from_path(path):
    return os.path.basename(path)

def get_xingqiji_by_datetime(date):
    if date.isoweekday() == 1:
        return "星期一"
    elif date.isoweekday() == 2:
        return "星期二"
    elif date.isoweekday() == 3:
        return "星期三"
    elif date.isoweekday() == 4:
        return "星期四"
    elif date.isoweekday() == 5:
        return "星期五"
    elif date.isoweekday() == 6:
        return "星期六"
    elif date.isoweekday() == 7:
        return "星期日"
    return "星期未知"


class TreeNode(object):
    def __init__(self, name):
        self.parent = None
        self.children = []
        self.name = name
        self.level = 0
        self.path = ""
        self.files = []

def get_days_of_month(year, month):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = 31
    elif month in [4, 6, 9, 11]:
        day = 30
    else:
        if (year % 100 == 0 and year % 400 == 0) or (year % 100 != 0 and year % 4 == 0):
            day = 29
        else:
            day = 28
    return day

def get_start_day_of_date(date):
    """
    
    :param date:  timedate 格式
    :return:
    """
    return f'{date.strftime("%Y-%m")}-01'

def get_last_day_of_date(date):
    day = get_days_of_month(date.year, date.month)
    return f'{date.strftime("%Y-%m")}-{day}'



if __name__ == "__main__":
    pass
