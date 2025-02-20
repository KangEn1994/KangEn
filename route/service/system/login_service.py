#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/7
import os, sys, re, json, traceback, time, hashlib
from route.entity.user import User
from route.service.database.sql_pool import SqlPool
from sqlalchemy import and_
from conf.conf import SALT, FERNET_KEY
from cryptography.fernet import Fernet

f = Fernet(FERNET_KEY)

class LoginService:
    @staticmethod
    def check_username_and_password(username, password):
        session = SqlPool.get_session()
        user = session.query(User).filter(and_(User.login_name == username, User.del_flag == User.DEL_NORMAL)).one()
        session.close()
        if user and user.password == password:
            return f.encrypt((username + SALT).encode())
        else:
            return False

    @staticmethod
    def update_password(new_password, username):
        session = SqlPool.get_session()
        user = session.query(User).filter(and_(User.login_name == username, User.del_flag == User.DEL_NORMAL)).one()
        user.password = new_password
        session.commit()
        session.close()

    @staticmethod
    def get_username_from_token(token):
        try:
            username = f.decrypt(token).decode()
            username = username[:len(username) - len(SALT)]
            return username
        except:
            return None

    @staticmethod
    def get_user_from_loginname(login_name):
        session = SqlPool.get_session()
        user = session.query(User).filter(and_(User.login_name == login_name, User.del_flag == User.DEL_NORMAL)).one()
        session.close()
        return user








if __name__ == "__main__":
    a = f.encrypt(("username" + SALT).encode())
    print(a)
    a = b'123'+ a + b'123'
    b = f.decrypt(a)
    print(b.decode())
