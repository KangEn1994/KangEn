#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/7
import os, sys, re, json, traceback, time, datetime
from route.entity.menu import Menu, MenuTree
from route.entity.menu_user_con import MenuUserCon
from route.entity.system.menu_role_con import MenuRoleCon
from route.service.database.sql_pool import SqlPool
from tools.utils.simple_utils import get_uuid
from route.service.system.login_service import LoginService, User
from route.service.config.role_service import RoleService, Role
from route.entity.role_user_con import RoleUserCon

class MenuService:
    @staticmethod
    def get_menu_tree_by_user(username, del_flag=True):
        session = SqlPool.get_session()
        # 首先要拿到所有的未删除菜单
        all_menu_list = session.query(Menu).filter(Menu.del_flag == Menu.DEL_NORMAL).all()
        # 其次要拿到该人有的所有菜单
        user = session.query(User).filter(User.login_name == username).one()
        # 拿到该人的所有角色
        role_list = session.query(Role).outerjoin(RoleUserCon).filter(RoleUserCon.user_id == user.id).all()
        print(role_list)
        user_menu_id_list = []
        for each_role in role_list:
            role_menu_list = session.query(Menu).outerjoin(MenuRoleCon).filter(MenuRoleCon.role_id == each_role.id).all()
            user_menu_id_list.extend([each.id for each in role_menu_list])
        user_menu_id_list = list(set(user_menu_id_list))
        # 将其构造成树形结构
        menu_tree = MenuTree.loads(all_menu_list)
        # 对该人没有权限的菜单进行忽略
        MenuTree.ignore_node(menu_tree, user_menu_id_list, del_flag=del_flag)
        # MenuTree.print_tree(menu_tree)
        session.close()
        return menu_tree

    @staticmethod
    def get_menu_by_id(menu_id):
        session = SqlPool.get_session()
        # 首先要拿到所有的未删除菜单
        menu = session.query(Menu).filter(Menu.id == menu_id).one()
        session.close()
        return menu

    @staticmethod
    def get_all_menu():
        session = SqlPool.get_session()
        # 首先要拿到所有的未删除菜单
        all_menu_list = session.query(Menu).filter(Menu.del_flag == Menu.DEL_NORMAL).all()
        # 将其构造成树形结构
        menu_tree = MenuTree.loads(all_menu_list)
        # 排序
        menu_tree.sort()
        session.close()
        return menu_tree

    @staticmethod
    def add_menu(name, describe, type, url, index, father_menu_id, user_name):
        user = LoginService.get_user_from_loginname(user_name)
        session = SqlPool.get_session()
        menu = Menu(id=get_uuid(), name=name, describe=describe, type=type, url=url, father_menu_id=father_menu_id,
                    index=index, create_by=user.id, update_by=user.id)
        session.add(menu)
        session.commit()
        session.close()

    @staticmethod
    def del_menu(menu_id):
        try:
            session = SqlPool.get_session()
            session.query(MenuUserCon).filter(MenuUserCon.menu_id == menu_id).delete()
            session.query(Menu).filter(Menu.id == menu_id).delete()
            session.commit()
            session.close()
            return True
        except:
            return False

    @staticmethod
    def update_menu(menu_id, name, describe, type, url, index, user_name):
        user = LoginService.get_user_from_loginname(user_name)
        session = SqlPool.get_session()
        menu = session.query(Menu).filter(Menu.id == menu_id).one()
        menu.name = name
        menu.describe = describe
        menu.type = type
        menu.url = url
        menu.index = index
        menu.update_by = user.id
        menu.update_time = datetime.datetime.now()
        session.commit()
        session.close()


    # MenuUserCon(id=get_uuid(), menu=each_menu, user=user, create_by="3771719ba7ac4cadbef73ccadfd04734", update_by="3771719ba7ac4cadbef73ccadfd04734")
    @staticmethod
    def update_menu_user_con(user_names, menu_ids, now_username):
        session = SqlPool.get_session()
        now_user = LoginService.get_user_from_loginname(now_username)
        user_names = user_names.split(",")
        menu_ids = menu_ids.split(",")
        menu_ids = [each for each in menu_ids if each]
        for each_user_name in user_names:
            # 删除掉原来的权限
            user = LoginService.get_user_from_loginname(each_user_name)
            session.query(MenuUserCon).filter(MenuUserCon.user_id == user.id).delete()
            for each_menu_id in menu_ids:
                each_menu = MenuService.get_menu_by_id(each_menu_id)
                menu_user_con = MenuUserCon(id=get_uuid(), menu=each_menu, user=user,  create_by=now_user.id, update_by=now_user.id)
                session.add(menu_user_con)
        session.commit()
        session.close()


# ==============================
    @staticmethod
    def get_menu_tree_by_role(role_id, del_flag=True):
        session = SqlPool.get_session()
        # 首先要拿到所有的未删除菜单
        all_menu_list = session.query(Menu).filter(Menu.del_flag == Menu.DEL_NORMAL).all()
        # 其次要拿到该人有的所有菜单
        role = session.query(Role).filter(Role.id == role_id).one()
        user_menu_list = session.query(Menu).outerjoin(MenuRoleCon).filter(MenuRoleCon.role_id == role.id).all()
        user_menu_id_list = [each.id for each in user_menu_list]
        # 将其构造成树形结构
        menu_tree = MenuTree.loads(all_menu_list)
        # 对该人没有权限的菜单进行忽略
        MenuTree.ignore_node(menu_tree, user_menu_id_list, del_flag=del_flag)
        # MenuTree.print_tree(menu_tree)
        session.close()
        return menu_tree

    @staticmethod
    def update_menu_role_con(role_ids, menu_ids, now_username):
        session = SqlPool.get_session()
        now_user = LoginService.get_user_from_loginname(now_username)
        role_ids = role_ids.split(",")
        menu_ids = menu_ids.split(",")
        menu_ids = [each for each in menu_ids if each]
        for each_role_id in role_ids:
            # 删除掉原来的权限
            role = RoleService.get_role_by_id(each_role_id)
            session.query(MenuRoleCon).filter(MenuRoleCon.role_id == role.id).delete()
            for each_menu_id in menu_ids:
                each_menu = MenuService.get_menu_by_id(each_menu_id)
                menu_role_con = MenuRoleCon(id=get_uuid(), menu=each_menu, role=role,  create_by=now_user.id, update_by=now_user.id)
                session.add(menu_role_con)
        session.commit()
        session.close()



if __name__ == "__main__":
    menu_tree = MenuService.get_menu_tree_by_user("zhangliang", del_flag=False)
    menu_list = menu_tree.to_list()
    for each in menu_list:
        # if each.boo:
        print("   "*each.level, each, each.children_num)
    # list.sort()

