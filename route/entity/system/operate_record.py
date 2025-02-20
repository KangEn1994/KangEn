#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2021/5/31 下午3:09
import os, sys, re, json, traceback, time, datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from route.entity.base import DeclarativeBase as Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class OperateRecord(Base):
    # 表名
    __tablename__ = "operate_record"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    # 表结构
    id = Column(Integer(), primary_key=True, autoincrement=True)  # id使用int自增即可
    url = Column(String(128))    # 访问的地址
    method = Column(String(16))    # 访问的方式
    username = Column(String(64))    # 访问的人
    create_time = Column(DateTime(), default=datetime.datetime.now)  # 创建时间




if __name__ == "__main__":
    from sqlalchemy import create_engine
    from conf.conf import MYSQL_PORT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, MYSQL_DATABASE

    engine = create_engine(
        'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
            MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE))
    Base.metadata.create_all(engine)

    # import datetime
    # from route.service.database.sql_pool import SqlPool
    #
    # session = SqlPool.get_session()
    # doc_type = Doc(doc_uuid="1.pdf", task_id=4, labeling_result="{}",
    #                    create_time=datetime.datetime.now(),
    #                    update_time=datetime.datetime.now())
    # session.add(doc_type)
    # session.commit()
    # session.close()

