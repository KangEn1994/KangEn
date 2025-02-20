#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/7
import os, sys, re, json, traceback, time
from route.service.database.sql_pool import SqlPool
from route.entity.operate_record import OperateRecord

class OperateRecordService:
    @staticmethod
    def add_record(url, method, username):
        session = SqlPool.get_session()
        operate_record = OperateRecord(url=url, method=method, username=username)
        session.add(operate_record)
        session.commit()
        session.close()


if __name__ == "__main__":
    pass
