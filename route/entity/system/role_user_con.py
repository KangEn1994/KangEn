#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2021/5/31 下午3:09
import os, sys, re, json, traceback, time
from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from route.entity.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from route.entity.system.role import Role


class RoleUserCon(Base):
    # 表名
    __tablename__ = "role_user_con"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    # 表结构
    role_id = Column(String(64), ForeignKey("role.id"))    # 菜单id
    user_id = Column(String(64), ForeignKey("user.id"))    # 用户id
    # type = Column(String(1))    # 菜单类型   父菜单0  直接链接1
    # url = Column(String(256))    # 链接地址
    # father_menu_id = Column(String(64), ForeignKey("menu.id"))    # 父级菜单id
    #
    # father_menu_id = relationship("Menu", backref="child_menu_list")

    role = relationship("Role", backref="role_user_con_list")
    user = relationship("User", backref="role_user_con_list")








if __name__ == "__main__":
    from sqlalchemy import create_engine
    from conf.conf import MYSQL_PORT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, MYSQL_DATABASE
    from route.entity.menu import Menu
    from route.entity.user import User
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

