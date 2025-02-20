#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/14
import os, sys, re, json, traceback, time, datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from route.entity.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Role(Base):
    # 表名
    __tablename__ = "role"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    boo = True
    # 表结构
    name = Column(String(64))    # 角色名
    describe = Column(String(256))    # 角色说明

    def __str__(self):
        return "角色id:{0},角色名称:{1},角色说明:{2},创建人:{3}".format(self.id, self.name, self.describe, self.create_by)


if __name__ == "__main__":
    pass
