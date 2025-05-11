#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/14
import os, sys, re, json, traceback, time, datetime
from route.service.database.sql_pool import SqlPool
from route.entity.system.role import Role
from route.entity.system.user import User
from tools.utils.simple_utils import get_uuid
from route.entity.system.role_user_con import RoleUserCon
from route.service.system.login_service import LoginService


class RoleService:
    @staticmethod
    def get_role_by_id(role_id):
        session = SqlPool.get_session()
        role = session.query(Role).filter(Role.id == role_id).one()
        session.close()
        return role

    @staticmethod
    def get_all_role():
        session = SqlPool.get_session()
        role_list = session.query(Role).all()
        return role_list

    @staticmethod
    def delete_role(role_id):
        try:
            session = SqlPool.get_session()
            session.query(Role).filter(Role.id == role_id).delete()
            session.commit()
            session.close()
            return True
        except:
            return False

    @staticmethod
    def update_role(role_id, name, describe, username):
        session = SqlPool.get_session()
        now_user = session.query(User).filter(User.login_name == username).one()
        role = session.query(Role).filter(Role.id == role_id).one()
        role.name = name
        role.describe = describe
        role.update_by = now_user.id
        role.update_time = datetime.datetime.now()
        session.commit()
        session.close()

    @staticmethod
    def add_role(name, describe, username):
        session = SqlPool.get_session()
        now_user = session.query(User).filter(User.login_name == username).one()
        role = Role(id=get_uuid(), name=name, describe=describe, create_by=now_user.id, update_by=now_user.id)
        session.add(role)
        session.commit()
        session.close()

    @staticmethod
    def get_role_of_user(user_id, del_flag=True):
        session = SqlPool.get_session()
        role_list = session.query(Role).outerjoin(RoleUserCon).filter(RoleUserCon.user_id == user_id).all()
        if not del_flag:
            all_role_list = session.query(Role).all()
            role_id_list = [each.id for each in role_list]
            for each in all_role_list:
                if each.id in role_id_list:
                    each.boo = True
                else:
                    each.boo = False
            role_list = all_role_list
        session.close()
        return role_list

    @staticmethod
    def update_role_user_con(user_names, role_ids, now_username):
        session = SqlPool.get_session()
        now_user = LoginService.get_user_from_loginname(now_username)
        user_names = user_names.split(",")
        role_ids = role_ids.split(",")
        role_ids = [each for each in role_ids if each]
        for each_user_name in user_names:
            # 删除掉原来的权限
            user = LoginService.get_user_from_loginname(each_user_name)
            session.query(RoleUserCon).filter(RoleUserCon.user_id == user.id).delete()
            for each_role_id in role_ids:
                each_role = RoleService.get_role_by_id(each_role_id)
                role_user_con = RoleUserCon(id=get_uuid(), role=each_role, user=user, create_by=now_user.id, update_by=now_user.id)
                session.add(role_user_con)
        session.commit()
        session.close()


if __name__ == "__main__":
    pass
