#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/9
from route.control.base_control import BaseControl
from flask import render_template, request, session
from route.service.config.user_service import UserService

class UserControl(BaseControl):
    def get(self):
        # 获取到当前所有的用户
        user_list = UserService.get_all_users()
        # redmine_user_list = RedmineUserService.get_xiake_user()
        # 返回并展示
        return render_template("config/user_list.html", user_list=user_list)

    def post(self):
        way = request.form["way"]
        if way == "add":  # 新增用户
            show_name = request.form["show_name"]
            login_name = request.form["login_name"]
            password = request.form["password"]
            UserService.add_user(show_name, login_name, password, session["username"])
            return "新增成功"
        elif way == "delete":   # 删除用户
            user_id = request.form["user_id"]
            boo = UserService.delete_user(user_id)
            if boo:
                return "删除成功"
            else:
                return "删除失败"
        elif way == "update":  # 修改密码
            user_id = request.form["user_id"]
            password = request.form["password"]
            remark = request.form["remark"]
            UserService.update_password(user_id, password, remark, session["username"])
            return "修改成功"
        else:
            return "参数错误"


if __name__ == "__main__":
    pass
