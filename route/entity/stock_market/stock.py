#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2021/5/31 下午3:09
import os, sys, re, json, traceback, time
from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from route.entity.base import Base


class Stock(Base):
    # 表名  股票表
    __tablename__ = "stock"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    # 表结构
    # id = Column(Integer(), primary_key=True, autoincrement=True)  # id使用uuid方便进行数据的迁移
    ts_code = Column(String(12))  # stock code
    ts_name = Column(String(8))
    ts_text = Column(Text())











if __name__ == "__main__":
    from sqlalchemy import create_engine
    from conf.conf import MYSQL_PORT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, MYSQL_DATABASE

    engine = create_engine(
        'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
            MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE))
    Base.metadata.create_all(engine)

    print("123")
