#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/8
import os, sys, re, json, traceback, time, datetime
from flask_restful import Resource
from route.control.base_control import BaseControl
from flask import Flask, request, send_file, render_template, redirect, make_response, request, session
from route.service.system.menu_service import MenuService
from route.service.system.login_service import LoginService
from tools.utils.simple_utils import get_xingqiji_by_datetime

class IndexControl(BaseControl):
    def get(self):
        # 获取当前用户
        username = session["username"]
        # 获取当前用户拥有的菜单
        menu_tree = MenuService.get_menu_tree_by_user(username)
        # 获取到展示名
        show_name = LoginService.get_user_from_loginname(username).show_name
        # 获取到日期
        now_time = datetime.datetime.now()
        now_time_str = now_time.strftime('%Y年%m月%d日')
        now_time_str += "  " + get_xingqiji_by_datetime(now_time)

        # 虽然之前的菜单设计都是不限制层数的，但是这里为了前端着想，设定只会存在两层的菜单结构
        return render_template("system/stock.html", menu_list=menu_tree.children, show_name=show_name, now_time=now_time_str)


class ShowIndexControl(BaseControl):
    def get(self):
        # 获取当前用户
        username = session["username"]
        # 获取到展示名
        show_name = LoginService.get_user_from_loginname(username).show_name
        # 获取到日期
        now_time = datetime.datetime.now()
        now_time_str = now_time.strftime('%Y年%m月%d日')
        return render_template("system/show.html", show_name=show_name, now_time=now_time_str)


class UpdatePasswordControl(BaseControl):
    def get(self):
        return render_template("system/update_password.html")

    def post(self):
        new_password = request.form["new_password"]
        # 获取当前用户
        username = session["username"]
        # 修改密码
        LoginService.update_password(new_password, username)
        session["token"] = ""
        return "修改成功"



if __name__ == "__main__":
    pass
