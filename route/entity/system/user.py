#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2021/5/31 下午3:09
import os, sys, re, json, traceback, time
from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from route.entity.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    # 表名
    __tablename__ = "user"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    # 表结构
    show_name = Column(String(64))    # 展示用户名
    login_name = Column(String(64))    # 登陆用户名
    password = Column(String(64))    # 密码

    # 由于扩展需求，将user 的remark字段设置为redmine_id 以用于和redmine系统数据进行对接

    def __str__(self):
        return "id={0}, name={1}".format(self.id, self.login_name)









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

