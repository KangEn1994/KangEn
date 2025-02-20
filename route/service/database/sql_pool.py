#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-11-20 15:09
import os, sys, re, json, traceback, time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from route.entity.base import Base
from conf.conf import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


class SqlPool:
    engine = create_engine(
        "mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8".format(
            MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE),
        max_overflow=10,  # 超过连接池大小外最多创建的连接
        pool_size=20,  # 连接池大小
        pool_timeout=20,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=0.5 * 60  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    )
    SessionFactory = sessionmaker(bind=engine)

    @staticmethod
    def get_session():
        return scoped_session(SqlPool.SessionFactory)

    @staticmethod
    def create_all():
        Base.metadata.create_all(SqlPool.engine)


if __name__ == "__main__":
    for i in range(19):
        print(id(SqlPool.get_session()))
