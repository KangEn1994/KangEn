#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time          : 2025/06/11 02:12
# @Author        : kang_en
# @Email         : kang_en@vip.qq.com
# @File          : scheduler_one.py
import os, sys, datetime, re, json

def run():
    from route.service.print_service import PrintService
    PrintService.print_daily_english_study()

