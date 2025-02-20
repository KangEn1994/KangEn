#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2021/5/31 下午3:09
import os, sys, re, json, traceback, time, datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from route.entity.base import DeclarativeBase as Base



class Log(Base):
    # 表名
    __tablename__ = "log"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    # 表结构
    id = Column(Integer(), primary_key=True, autoincrement=True)  # id使用int自增即可
    type = Column(String(1))    # 日志类型   定时任务日志0
    title = Column(String(64))    # 日志标题
    describe = Column(Text())    # 日志表述
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

