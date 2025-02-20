#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2021/5/31 下午3:09
import os, sys, re, json, traceback, time
from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from route.entity.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from tools.utils.simple_utils import get_uuid

class Dict(Base):
    # 表名  字典表
    __tablename__ = "dict"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    # 表结构
    name = Column(String(64))    # 类型名称
    key = Column(String(64))    # key
    value = Column(String(64))    # value


"""
name=score               个人分值类别
name=group               组加分项分类
name=project_status      项目状态     



"""









if __name__ == "__main__":
    from sqlalchemy import create_engine
    from conf.conf import MYSQL_PORT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, MYSQL_DATABASE

    engine = create_engine(
        'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
            MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE))
    Base.metadata.create_all(engine)
    #
    # import datetime
    # from route.service.database.sql_pool import SqlPool
    # #
    # session = SqlPool.get_session()
    # d1 = Dict(id=get_uuid(), name="project_status", key="01", value="POC", create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
    # d2 = Dict(id=get_uuid(), name="project_status", key="02", value="售前", create_time=datetime.datetime.now(),
    #           update_time=datetime.datetime.now())
    # d3 = Dict(id=get_uuid(), name="project_status", key="03", value="POC完成", create_time=datetime.datetime.now(),
    #           update_time=datetime.datetime.now())
    # d4 = Dict(id=get_uuid(), name="project_status", key="04", value="未签单", create_time=datetime.datetime.now(),
    #           update_time=datetime.datetime.now())
    # d5 = Dict(id=get_uuid(), name="project_status", key="05", value="交付中", create_time=datetime.datetime.now(),
    #           update_time=datetime.datetime.now())
    # d6 = Dict(id=get_uuid(), name="project_status", key="06", value="维保中", create_time=datetime.datetime.now(),
    #           update_time=datetime.datetime.now())
    # session.add(d1)
    # session.add(d2)
    # session.add(d3)
    # session.add(d4)
    # session.add(d5)
    # session.add(d6)
    #
    #
    # session.commit()
    # session.close()
    #
