#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time          : 2025/05/11 20:39
# @Author        : kang_en
# @Email         : kang_en@vip.qq.com
# @File          : name_service.py
import os, sys, datetime, re, json, random
import traceback, time

with open("doc/hanzi.txt", "r", encoding="utf-8") as f:
    hanzi_str = f.readline()
    xing_list = f.readline().split(",")

class NameService:

    @staticmethod
    def get_name_of_person():
        """
        随机生成一个名字
        :return:
        """
        name_list = []
        for i in range(100):
            name = random.choice(xing_list) + random.choice(hanzi_str) + random.choice(hanzi_str)
            name_list.append(name)
        
        return name_list
    

    def get_name_of_thing(length=4):
        """
        随机生成一个名字
        :return:
        """
        name_list = []
        for i in range(100):
            name = random.choice(hanzi_str) + random.choice(hanzi_str) + random.choice(hanzi_str) + random.choice(hanzi_str)
            name_list.append(name)
        return name_list

