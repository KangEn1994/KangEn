#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time          : 2025/05/11 21:01
# @Author        : kang_en
# @Email         : kang_en@vip.qq.com
# @File          : name_control.py
import os, sys, datetime, re, json
import traceback, time


from flask import render_template, request, session, jsonify
from route.control.base_control import BaseControl
from route.service.novel.name_service import NameService


class NameControl(BaseControl):
    def get(self):
        return render_template('novel/name.html')

    def post(self):
        t = request.form.get("way", None)

        name_list = []
        if t == "1":
            name_list = NameService.get_name_of_person()
        elif t == "2":
            name_list = NameService.get_name_of_thing()
        

        return "\t".join(name_list)



class ZiControl(BaseControl):
    def get(self):
        return render_template('novel/zi.html')

    def post(self):
        t = request.form.get("zi", "")

        with open("doc/hanzi.txt", "r", encoding="utf-8") as f:
            hanzi_str = f.readline()
            xing_list = f.readline()
        
        print(f"删除前长度: {len(hanzi_str)}")
        for e in t:
            hanzi_str = hanzi_str.replace(e, "")
        
        with open("doc/hanzi.txt", "w", encoding="utf-8") as f:
            f.write(hanzi_str)
            f.write(xing_list)
        
        print(f"删除后长度: {len(hanzi_str)}")
        return True
