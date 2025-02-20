#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/8
from route.control.base_control import BaseControl
from flask import render_template, request, session
from route.service.system.menu_service import MenuService
from route.service.config.user_service import UserService
from route.service.config.role_service import RoleService
from route.service.system.login_service import LoginService

class MenuControl(BaseControl):
    def get(self):
        # 展示出当前已有的所有菜单信息
        menu_tree = MenuService.get_all_menu()
        # 整理父节点的关系表，方便进行父节点隐藏
        menu_tree.add_parent_list()
        # 将其整理成list的形式便于展示
        menu_list = menu_tree.to_list()
        # 返回并展示
        return render_template("config/menu_list.html", menu_list=menu_list)

    def post(self):
        # 对当前菜单进行修改  这个接口最好采用ajax进行修改
        way = request.form["way"]
        if way == "add":
            parent_id = request.form["parent_id"]
            name = request.form["name"]
            describe = request.form["describe"]
            type = request.form["type"]
            url = request.form["url"]
            index = request.form["index"]
            MenuService.add_menu(name, describe, type, url, index, parent_id, session["username"])
            return "新增成功"
        elif way == "del":
            menu_id = request.form["id"]
            boo = MenuService.del_menu(menu_id)
            if boo:
                return "删除成功"
            else:
                return "尚存在子菜单，无法删除"
        elif way == "update":
            menu_id = request.form["menu_id"]
            name = request.form["name"]
            describe = request.form["describe"]
            type = request.form["type"]
            url = request.form["url"]
            index = request.form["index"]
            MenuService.update_menu(menu_id, name, describe, type, url, index, session["username"])
            return "修改成功"
        else:
            return None

class MenuUserConControl(BaseControl):
    def get(self):
        username = request.args.get("username", None)
        if not username:
            username = session["username"]
        # 1.获取所有用户方便根据用户来进行菜单查询，默认是自己
        users = UserService.get_all_users()
        # 2.根据默认用户查询该用户的菜单   要求是所有菜单打钩的形式
        menu_tree = MenuService.get_menu_tree_by_user(username, del_flag=False)
        # 将其整理成list的形式便于展示
        menu_list = menu_tree.to_list()
        return render_template("config/menu_user_con.html", users=users, menu_list=menu_list, username=username)

    def post(self):
        user_names = request.form["user_names"]
        menu_ids = request.form["menu_ids"]
        now_username = session["username"]
        MenuService.update_menu_user_con(user_names, menu_ids, now_username)
        return "更新完成"

class MenuRoleConControl(BaseControl):
    def get(self):
        role_id = request.args.get("role_id", None)
        username = session["username"]
        if not role_id:
            role_id = "1"
        # 1.获取所有用户方便根据用户来进行菜单查询，默认是自己
        roles = RoleService.get_all_role()
        # 2.根据默认用户查询该用户的菜单   要求是所有菜单打钩的形式
        menu_tree = MenuService.get_menu_tree_by_role(role_id, del_flag=False)
        # 将其整理成list的形式便于展示
        menu_list = menu_tree.to_list()
        return render_template("config/menu_role_con.html", roles=roles, menu_list=menu_list, role_id=role_id)

    def post(self):
        role_ids = request.form["role_ids"]
        menu_ids = request.form["menu_ids"]
        now_username = session["username"]
        MenuService.update_menu_role_con(role_ids, menu_ids, now_username)
        return "更新完成"

if __name__ == "__main__":
    pass
