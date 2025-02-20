#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/14
import os, sys, re, json, traceback, time, datetime
from route.control.base_control import BaseControl
from flask import render_template, request, session
from route.service.config.role_service import RoleService
from route.service.config.user_service import UserService
from route.service.system.login_service import LoginService

class RoleControl(BaseControl):
    def get(self):
        # 展示出当前已有的所有角色信息
        role_list = RoleService.get_all_role()
        # 返回并展示
        return render_template("config/role_list.html", role_list=role_list)

    def post(self):
        # 对当前角色进行修改  这个接口最好采用ajax进行修改
        way = request.form["way"]
        if way == "add":
            name = request.form["name"]
            describe = request.form["describe"]
            RoleService.add_role(name, describe, session["username"])
            return "新增成功"
        elif way == "delete":
            role_id = request.form["role_id"]
            boo = RoleService.delete_role(role_id)
            if boo:
                return "删除成功"
            else:
                return "尚存在子菜单，无法删除"
        elif way == "update":
            role_id = request.form["role_id"]
            name = request.form["name"]
            describe = request.form["describe"]
            RoleService.update_role(role_id, name, describe, session["username"])
            return "修改成功"
        else:
            return None


class RoleUserControl(BaseControl):
    def get(self):
        username = request.args.get("username", None)
        if not username:
            username = session["username"]
        # 1.获取所有用户方便根据用户来进行菜单查询，默认是自己
        users = UserService.get_all_users()
        user = LoginService.get_user_from_loginname(username)
        # 2.根据默认用户查询该用户的菜单   要求是所有菜单打钩的形式
        role_list = RoleService.get_role_of_user(user_id=user.id, del_flag=False)
        return render_template("config/role_user_con.html", users=users, role_list=role_list, user=user)

    def post(self):
        user_names = request.form["user_names"]
        role_ids = request.form["role_ids"]
        now_username = session["username"]
        RoleService.update_role_user_con(user_names, role_ids, now_username)
        return "更新完成"




if __name__ == "__main__":
    pass
