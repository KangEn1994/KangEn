#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-11-18 14:50
import datetime

from route.service.system.login_service import LoginService
import _locale

_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

from flask import Flask, send_file, render_template, make_response, request, session
from flask_restful import Api
from flask_apscheduler import APScheduler

app = Flask(__name__, template_folder="template/")
app.config['SECRET_KEY'] = "I love you."


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.before_request
def before_request():
    pass_url_start_list = ["/static", "/public"]
    url = request.path
    # 静态文件的访问不需要进行记录
    for each in pass_url_start_list:
        if url.startswith(each):
            return
    # 1.我们要获取到登陆的账户和密码
    username, password = request.args.get("username", None), request.args.get("password", None)
    if username and password:
        token = LoginService.check_username_and_password(username, password)
        if token:
            session["token"] = token
        else:
            return "账号或密码错误"
    token = session.get("token", None)
    if not token:
        return "尚未登陆"
    username = LoginService.get_username_from_token(token)
    if not username:
        return "token出错请重新登陆"
    session["username"] = username
    # 已经获取到当前登陆用户 username
    # 2.对当前用户的操作进行记录    id, url, method, username, create_time
    # 暂时不记录接口操作记录了，太浪费时间了
    # OperateRecordService.add_record(url, request.method, username)







api = Api(app)


@api.representation("text/html")
def out_html(data, code, headers=None):
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp



@app.route('/static/js/<path:path>', methods=['GET'])
def js_file(path):
    return send_file('template/js/{0}'.format(path))

@app.route('/static/doc/<path:path>', methods=['GET'])
def doc_file(path):
    return send_file('doc/{0}'.format(path))

@app.route('/static/css/<path:path>', methods=['GET'])
def css_file(path):
    return send_file('template/css/{0}'.format(path))


@app.route('/static/img/<path:path>', methods=['GET'])
def img_file(path):
    return send_file('template/img/{0}'.format(path))


@app.route('/static/images/<path:path>', methods=['GET'])
def images_file(path):
    return send_file('template/img/{0}'.format(path))


@app.route('/static/fonts/<path:path>', methods=['GET'])
def fonts_file(path):
    return send_file('template/fonts/{0}'.format(path))


@app.route('/static/md/<path:path>', methods=['GET'])
def md_file(path):
    return send_file('template/idps/markdown/{0}'.format(path))


@app.route('/staticfile/<path:path>', methods=['GET'])
def staticfile(path):
    return send_file('template/{0}'.format(path))


@app.route('/markdown/<path:path>', methods=['GET'])
def markdown_show(path):
    # /markdown/idps/markdown/readme.md
    return render_template('markdown_show.html', markdown_file_path=path)


@app.route('/pdf/<path:filename>', methods=['GET'])
def pdf_file(filename):
    # /markdown/idps/markdown/readme.md
    return send_file('files/{0}'.format(filename))

from tools.utils.template_utils import get_length
app.add_template_filter(get_length, 'get_length')

# from tools.utils.template_utils import get_length
app.add_template_filter(str, 'str')


# 样例
# from  xxxx  import zzzz
#

# 访问首页
from route.control.system.index_control import IndexControl, ShowIndexControl, UpdatePasswordControl
api.add_resource(IndexControl, '/')
api.add_resource(ShowIndexControl, '/show')
api.add_resource(UpdatePasswordControl, '/update_password')
from route.control.system.log_control import LogControl
api.add_resource(LogControl, '/log')


# 菜单部分
from route.control.system.menu_control import MenuControl, MenuUserConControl, MenuRoleConControl
api.add_resource(MenuControl, "/menu/menu")
api.add_resource(MenuUserConControl, "/menu/menu_user_con")
api.add_resource(MenuRoleConControl, "/menu/menu_role_con")

# 角色部分
from route.control.config.role_control import RoleControl, RoleUserControl
api.add_resource(RoleControl, "/role/role")
api.add_resource(RoleUserControl, "/role/role_user_con")
# 用户部分
from route.control.config.user_control import UserControl
api.add_resource(UserControl, "/config/user")


# 股票部分
from route.control.stock_market.stock_control import StockControl
api.add_resource(StockControl, "/stock/stock/<string:code>", "/stock/stock")


# 小说部分
from route.control.novel.name_control import NameControl, ZiControl
api.add_resource(ZiControl, "/novel/zi")
api.add_resource(NameControl, "/novel/name")


# 学习部分
from route.control.study.english_sentence_control import EnglishSentenceControl
api.add_resource(EnglishSentenceControl, "/study/english_sentence")


#  定时任务部分
class Config(object):
    SCHEDULER_API_ENABLED = True


scheduler = APScheduler()


@scheduler.task('cron', id='task1', day='*', hour='03', minute='00', second='00')
def task1():  # 每天凌晨3点跑一次
    pass


@scheduler.task('cron', id='task2', day='*', hour='20', minute='00', second='00')
def task2():  # 每天晚上8点跑一次
    pass


@scheduler.task('cron', id='task3', day='*', hour='13', minute='00', second='00')
def task3():  # 每天下午1点跑一次，看看谁的每日计划没有写
    pass

@scheduler.task('cron', id='task4', day='*', hour='21', minute='00', second='00')
def task4():  # 第一个休息日晚上9点跑一次，看看谁的redmine没有写
    pass   # 后面再写，逻辑和之前有点类似




if __name__ == "__main__":
    # 启动
    # app.config['JSON_AS_ASCII'] = False
    # app.run(port=9999, host='0.0.0.0')
    # init()


    app.config.from_object(Config())
    app.config['JSON_AS_ASCII'] = False
    scheduler.init_app(app)
    scheduler.start()
    app.run(port=9999, host='0.0.0.0')
