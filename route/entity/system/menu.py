#!/usr/bin/env python
# coding=utf-8
# author:jingjian@datagrand.com
# datetime:2021/5/31 下午3:09
import os, sys, re, json, traceback, time
from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from route.entity.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Menu(Base):
    # 表名
    __tablename__ = "menu"
    __table_args__ = {
        'mysql_charset': 'utf8'
    }
    MENU_TYPE_MENU = 0
    MENU_TYPE_URL = 1
    MENU_TYPE_TANCHUANG = 2
    level = 0
    parent_str = ""
    children_num = 0
    boo = True   # 该菜单是否可见
    TOP_MENU_ID = "1"   # 顶节点的id
    # 表结构
    name = Column(String(16))    # 展示菜单名
    describe = Column(String(64))    # 菜单介绍
    type = Column(String(1))    # 菜单类型   父菜单0  直接链接1   弹窗展示2
    url = Column(String(256))    # 链接地址
    index = Column(Integer())   # 顺序
    father_menu_id = Column(String(64))    # 父级菜单id


    # father_menu = relationship("Menu", backref="child_menu_list")

    def __str__(self):
        return "id={0}, name={1}".format(self.id, self.name)

    def __cmp__(self, other):
        if self.index < other.index:
            return -1
        elif self.index == other.index:
            return 0
        else:
            return 1

    def __lt__(self, other):
        return self.index < other.index

    def __eq__(self, other):
        if self.name == other.name and self.describe == other.describe and self.type == other.type \
                and self.url == other.url and self.index == other.index and self.father_menu_id == other.father_menu_id \
                and self.id == other.id and self.remark == other.remark and self.del_flag == other.del_falg:
            return True
        else:
            return False


class MenuTree():
    def __init__(self, menu):
        self.menu = menu
        self.children = []
        self.parent = None

    def __cmp__(self, other):
        return self.menu.__cmp__(other.menu)

    def __lt__(self, other):
        return self.menu.index < other.menu.index

    @staticmethod
    def loads(menu_list):
        # 将菜单列表加载成菜单树的形式
        menu_tree_list = [MenuTree(each) for each in menu_list]
        menu_tree_dict = {each.menu.id: each for each in menu_tree_list}
        for each in menu_tree_list:
            if each.menu.id == Menu.TOP_MENU_ID:
                continue
            if each.menu.father_menu_id == Menu.TOP_MENU_ID:
                menu_tree_dict[Menu.TOP_MENU_ID].children.append(each)
            elif each.menu.father_menu_id:
                menu_tree_dict[each.menu.father_menu_id].children.append(each)
                each.parent = menu_tree_dict[each.menu.father_menu_id]
        menu_tree_dict[Menu.TOP_MENU_ID].sort()
        return menu_tree_dict[Menu.TOP_MENU_ID]

    @staticmethod
    def ignore_node(menu_tree, id_list, del_flag=True):
        # 从菜单树 的叶子节点中忽略所有不在id_list中的叶子节点
        if menu_tree.children:
            if del_flag:
                menu_tree.children = [each for each in menu_tree.children if MenuTree.ignore_node(each, id_list, del_flag=del_flag)]
                true_children = menu_tree.children
            else:
                true_children = [each for each in menu_tree.children if MenuTree.ignore_node(each, id_list, del_flag=del_flag)]
            if true_children:
                # menu_tree.children.sort()
                menu_tree.menu.boo = True
            else:
                menu_tree.menu.boo = False
        else:
            if menu_tree.menu.id in id_list:
                menu_tree.menu.boo = True
            else:
                menu_tree.menu.boo = False
        return menu_tree.menu.boo

    def sort(self):
        self.children.sort()
        for each in self.children:
            each.sort()

    def to_list(self, menu_list=None, level=0):
        if not menu_list:
            menu_list = list()
        self.menu.children_num = len(self.children)
        for each in self.children:
            each.menu.level = level
            menu_list.append(each.menu)
            each.to_list(menu_list=menu_list, level=level + 1)
        return menu_list

    def add_parent_list(self):
        # 增设历史父节点id.用于隐藏对应子节点
        for each in self.children:
            each.menu.parent_str += self.menu.parent_str + " " + self.menu.id
            each.add_parent_list()


    @staticmethod
    def print_tree(menu_tree, index=0):
        "缩进打印"
        print("  "*index + menu_tree.menu.name + "(" + menu_tree.menu.id + ")")
        for each in menu_tree.children:
            if each.menu.boo:
                MenuTree.print_tree(each, index=index+1)











if __name__ == "__main__":
    from sqlalchemy import create_engine
    from conf.conf import MYSQL_PORT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, MYSQL_DATABASE

    engine = create_engine(
        'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
            MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE))
    Base.metadata.create_all(engine)

    # import datetime
    # from route.service.database.sql_pool import SqlPool
    #
    # session = SqlPool.get_session()
    # doc_type = Doc(doc_uuid="1.pdf", task_id=4, labeling_result="{}",
    #                    create_time=datetime.datetime.now(),
    #                    update_time=datetime.datetime.now())
    # session.add(doc_type)
    # session.commit()
    # session.close()

