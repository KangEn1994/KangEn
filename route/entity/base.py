#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-11-20 14:42
import os, sys, re, json, traceback, time, datetime
from sqlalchemy.ext.declarative import declarative_base
import _locale
from tools.utils.simple_utils import get_uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

# 创建对象的基类:
DeclarativeBase = declarative_base()



class Base(DeclarativeBase):
    __abstract__ = True
    DEL_NORMAL = 0
    DEL_DELETE = 1
    id = Column(String(64), primary_key=True)  # id使用uuid方便进行数据的迁移
    remark = Column(Text())  # 备注
    del_flag = Column(String(1), default="0")   # 删除标记  0正常   1删除
    create_by = Column(String(64))  # 创建者ID
    create_time = Column(DateTime(), default=datetime.datetime.now)  # 创建时间
    update_by = Column(String(64))  # 修改者ID
    update_time = Column(DateTime(), default=datetime.datetime.now)  # 修改时间





if __name__ == "__main__":
    pass
