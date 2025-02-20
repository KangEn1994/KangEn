#!/usr/bin/env python
# coding=utf-8
# author:uncleyiba@qq.com
# datetime:2024/1/26 17:03
import os, sys, re, json, traceback, time

import smtplib
from email.mime.text import MIMEText




def send_email(to, title, text):
    pass

    """ 因为邮箱现在要三个月改一次密码，懒得弄了，所以不搞邮件发送了
    server = smtplib.SMTP('', 25)
    server.starttls()
    server.login('', '')
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = title
    msg['From'] = ''
    msg['To'] = to
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.close()
    """
