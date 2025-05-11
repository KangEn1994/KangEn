#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/8
import os, sys, re, json, traceback, time, datetime
from route.entity.system.user import User
from route.entity.system.role_user_con import RoleUserCon
from route.service.database.sql_pool import SqlPool
from tools.utils.simple_utils import get_uuid

class UserService:
    @staticmethod
    def get_all_users():
        session = SqlPool.get_session()
        users = session.query(User).all()
        session.close()
        return users

    @staticmethod
    def get_user_by_id(user_id):
        session = SqlPool.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        session.close()
        return user

    @staticmethod
    def get_users_by_role_id(role_id):
        session = SqlPool.get_session()
        cons= session.query(RoleUserCon).filter(RoleUserCon.role_id == role_id).all()
        users = [e.user for e in cons]
        session.close()
        return users

    @staticmethod
    def get_users_by_show_name(show_name):
        session = SqlPool.get_session()
        user = session.query(User).filter(User.show_name == show_name).first()
        session.close()
        return user

    @staticmethod
    def get_users_by_login_name(show_name):
        session = SqlPool.get_session()
        user = session.query(User).filter(User.login_name == show_name).first()
        session.close()
        return user

    @staticmethod
    def delete_user(user_id):
        try:
            session = SqlPool.get_session()
            session.query(User).filter(User.id == user_id).delete()
            session.commit()
            session.close()
            return True
        except:
            print(traceback.format_exc())
            return False

    @staticmethod
    def update_password(user_id, new_password, remark,  username):
        session = SqlPool.get_session()
        now_user = session.query(User).filter(User.login_name == username).one()
        user = session.query(User).filter(User.id == user_id).one()
        user.password = new_password
        user.remark = remark
        user.update_by = now_user.id
        user.update_time = datetime.datetime.now()
        session.commit()
        session.close()

    @staticmethod
    def add_user(show_name, login_name, password, username):
        session = SqlPool.get_session()
        now_user = session.query(User).filter(User.login_name == username).one()
        user = User(id=get_uuid(), login_name=login_name, show_name=show_name, password=password, create_by=now_user.id, update_by=now_user.id)
        session.add(user)
        session.commit()
        session.close()

if __name__ == "__main__":
    pass
