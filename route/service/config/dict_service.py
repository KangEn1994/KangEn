#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/11
import os, sys, re, json, traceback, time, datetime
from route.service.database.sql_pool import SqlPool
from tools.utils.simple_utils import get_uuid
from route.entity.dict import Dict
from route.entity.user import User
from route.entity.company import Company

class DictService:
    @staticmethod
    def get_target_dict(name):
        session = SqlPool.get_session()
        persons = session.query(Dict).filter(Dict.name == name).order_by(Dict.create_time).all()
        session.close()
        return persons


    @staticmethod
    def add(name, key, value, username):
        session = SqlPool.get_session()
        now_user = session.query(User).filter(User.login_name == username).one()
        dict = Dict(id=get_uuid(), name=name, key=key, value=value, create_by=now_user.id, update_by=now_user.id)
        session.add(dict)
        session.commit()
        session.close()

    @staticmethod
    def update(dict_id, name, key, value, username):
        session = SqlPool.get_session()
        now_user = session.query(User).filter(User.login_name == username).one()
        dict = session.query(Dict).filter(Dict.id == dict_id).one()
        dict.name = name
        dict.company = key
        dict.post = value
        dict.update_by = now_user.id
        dict.update_time = datetime.datetime.now()
        session.commit()
        session.close()

    @staticmethod
    def delete(dict_id, username):
        try:
            session = SqlPool.get_session()
            now_user = session.query(User).filter(User.login_name == username).one()
            dict = session.query(Dict).filter(Dict.id == dict_id).one()
            dict.del_flag = Dict.DEL_DELETE
            dict.update_by = now_user.id
            dict.update_time = datetime.datetime.now()
            session.commit()
            session.close()
            return True
        except:
            return False



if __name__ == "__main__":
    # DictService.add("score", "01", "每日计划填写不及时1", "jingjian")
    # DictService.add("score", "02", "表扬信2", "jingjian")
    # DictService.add("score", "03", "数据沉淀5", "jingjian")
    # DictService.add("score", "04", "业务流程沉淀2", "jingjian")
    # DictService.add("score", "05", "每周之星3", "jingjian")
    # DictService.add("score", "06", "资质证书2/5/10", "jingjian")
    # DictService.add("score", "07", "文章撰写2", "jingjian")
    # DictService.add("score", "08", "专利3", "jingjian")
    # DictService.add("score", "09", "项目评估1", "jingjian")
    # DictService.add("score", "10", "技术分享2", "jingjian")
    # DictService.add("score", "11", "季度奖5", "jingjian")
    # DictService.add("score", "12", "POC主导2", "jingjian")
    # DictService.add("score", "13", "功能回流产品5", "jingjian")
    # DictService.add("score", "14", "工作承接1", "jingjian")
    # DictService.add("score", "15", "疑难杂症解决2", "jingjian")
    # DictService.add("score", "16", "组内比赛第一5", "jingjian")
    # DictService.add("score", "17", "组织技术培训过5", "jingjian")
    # DictService.add("score", "18", "文档整理1-10", "jingjian")
    # DictService.add("score", "19", "客户合理投诉1-10", "jingjian")
    # DictService.add("score", "20", "redmine填写不及时2", "jingjian")
    # DictService.add("score", "21", "项目问题1-10", "jingjian")
    # DictService.add("score", "22", "培训/比赛缺席2", "jingjian")
    # DictService.add("score", "23", "集体活动缺席1", "jingjian")
    DictService.add("score", "99", "其他", "jingjian")


