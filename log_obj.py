#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-11-18 14:47
import os, sys, re, json, traceback, time, logging
import _locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

filename = os.path.join(os.path.dirname(__file__), 'log/root.log')
print(filename)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# fileHandler = logging.StreamHandler()
fileHandler = logging.FileHandler(filename=filename)
formatter = logging.Formatter(
    fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    datefmt='%y-%m-%d %H:%M:%S %z'
)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


def log_print(log_moudle, message, log_type="info", end="\n"):
    if log_type == "info":
        log_moudle.info(message)
        print(message, end=end)
    else:
        log_moudle.error(message)
        print(message, end=end)


if __name__ == "__main__":
    pass