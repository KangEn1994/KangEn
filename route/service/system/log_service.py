#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/7
from route.service.database.sql_pool import SqlPool
from route.entity.system.log import Log
from sqlalchemy import func, and_

class LogService:
    @staticmethod
    def add_log(type, title, describe):
        session = SqlPool.get_session()
        log = Log(type=type, title=title, describe=describe)
        session.add(log)
        session.commit()
        session.close()

    @staticmethod
    def get_all_by_type(type, title, page_num, page_size):
        session = SqlPool.get_session()
        log_list = session.query(Log).filter(and_(Log.type == type, Log.title.like(f"%{title}%"))).order_by(
            Log.id.desc()).limit(page_size).offset(
            page_num * page_size - page_size).all()
        total = session.query(func.count(Log.id)).filter(
            Log.type == type).scalar()
        session.close()
        return log_list, total



if __name__ == "__main__":
    # LogService.add_log("0", "title1", "describe1")
    # time.sleep(1)
    # LogService.add_log("0", "title2", "describe2")
    # time.sleep(1)
    # LogService.add_log("0", "title3", "describe3")
    # time.sleep(1)
    # LogService.add_log("0", "title4", "describe4")
    # time.sleep(1)
    # LogService.add_log("0", "title5", "describe5")
    # time.sleep(1)
    a, b = LogService.get_all_by_type("0", 1, 20)
    for e in a:
        print(e.describe)
