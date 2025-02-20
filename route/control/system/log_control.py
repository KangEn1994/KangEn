#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/11
from flask import render_template, request, session
from route.control.base_control import BaseControl
from route.service.system.log_service import LogService


class LogControl(BaseControl):
    def get(self):
        type = request.args.get("type", "0")
        title = request.args.get("title", "")
        page_num = int(request.args.get("page_num", "1"))
        page_size = int(request.args.get("page_size", "20"))
        log_list, total = LogService.get_all_by_type(type, title, page_num, page_size)
        return render_template("system/log.html", type=type, page_num=page_num, page_size=page_size, log_list=log_list,
                               total=total)


if __name__ == "__main__":
    pass
