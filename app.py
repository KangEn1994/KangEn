#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2020-11-18 14:50
import datetime
import threading
import traceback

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


# @app.route('/', methods=['GET'])
# def app_html():
#     user = request.args.get("user", "")
#     conf_file = open("conf/menu.txt", "r")
#     menu_data = conf_file.read().split("\n")
#     conf_file.close()
#     menu_info = []
#     for each in menu_data:
#         if not each.startswith("#"):
#             each_menu = each.split(",")
#             if len(each_menu) == 4:
#                 menu_info.append(each_menu)
#             elif len(each_menu) == 3:
#                 each_menu.append("show_iframe")
#                 menu_info.append(each_menu)
#
#     return render_template("index.html", menu_info=menu_info)


@app.route('/static/js/<path:path>', methods=['GET'])
def js_file(path):
    return send_file('template/js/{0}'.format(path))


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
# api.add_resource(IndexControl, '/')
api.add_resource(ShowIndexControl, '/show')
api.add_resource(UpdatePasswordControl, '/update_password')
from route.control.system.log_control import LogControl
api.add_resource(LogControl, '/log')
# 事项中心
from route.control.routine.redmine_control import RedmineControl
from route.control.routine.daily_control import DailyControl
from route.control.routine.routine_control import UrlInfoControl, InfoShowControl
api.add_resource(RedmineControl, "/routine/redmine", "/public/redmine")
api.add_resource(DailyControl, "/routine/daily")
api.add_resource(UrlInfoControl, "/routine/urlinfo")
api.add_resource(InfoShowControl, "/routine/infoshow")

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

# 公司部分
from route.control.config.company_control import CompanyControl
api.add_resource(CompanyControl, "/config/company")
# 公司人员
# from route.control.config.person_control import PersonControl, PersonByCompanyControl
# api.add_resource(PersonControl, "/config/person", "/info/person")
# api.add_resource(PersonByCompanyControl, "/ajax/person_by_company")

# 项目部分
# from route.control.project.project_control import ProjectControl, ProjectDetailControl, ProjectDetailInfoControl, ProjectPersonControl
# api.add_resource(ProjectControl, "/config/project")
# api.add_resource(ProjectDetailControl, "/config/project_detail")
# api.add_resource(ProjectDetailInfoControl, "/info/project_detail")
# api.add_resource(ProjectPersonControl, '/ajax/person_by_project')

# license管理
from route.control.redmine.redmine_license_record_control import RedmineLicenseRecordWarningControl, RedmineLicenseRecordControl
api.add_resource(RedmineLicenseRecordControl, "/config/license")
api.add_resource(RedmineLicenseRecordWarningControl, "/config/license_warning")



# 分值奖励
from route.control.routine.score_record_control import ScoreRecordControl
api.add_resource(ScoreRecordControl, "/routine/score_record")
from route.control.routine.group_score_record_control import GroupScoreRecordControl
api.add_resource(GroupScoreRecordControl, "/routine/group_score_record", "/public/group_score_record")



# 项目业绩详情展示
# from route.control.config.project_yeji_control import ProjectYejiControl, ProjectYejiDetailControl
# api.add_resource(ProjectYejiControl, "/config/project_yeji")
# api.add_resource(ProjectYejiDetailControl, "/config/project_yeji_detail")


from route.control.idps.info_show import InfoShow, DetailShow, FileShow
from route.control.idps.info_search import InfoSearch
api.add_resource(InfoShow, '/idps/infoshow')
api.add_resource(InfoSearch, '/idps/infosearch')
api.add_resource(DetailShow, '/idps/showinfo/<uuid>')
api.add_resource(FileShow, '/idps/fileshow/<uuid>')


from route.control.redmine.redmine_project_control import RedmineProjectControl, RedmineProjectDetailControl
from route.control.redmine.redmine_user_control import RedmineUserControl
from route.control.redmine.redmine_title_control import RedmineTitleControl
from route.control.redmine.redmine_payment_control import RedminePaymentControl, RedminePaymentMonthControl
api.add_resource(RedmineProjectControl, '/redmine/projects')
api.add_resource(RedmineProjectDetailControl, '/redmine/project_detail')
api.add_resource(RedmineUserControl, '/redmine/users')
api.add_resource(RedmineTitleControl, '/redmine/user_title')
api.add_resource(RedminePaymentControl, '/redmine/project_back_money')
api.add_resource(RedminePaymentMonthControl, '/redmine/month_back_money')


# 工时统计
from route.control.redmine.redmine_entry_control import RedmineEntryPersonControl, RedmineEntryProjectControl, RedmineEntryGroupControl
api.add_resource(RedmineEntryPersonControl, '/redmine/user_time_entry')
api.add_resource(RedmineEntryProjectControl, '/redmine/project_time_entry')
api.add_resource(RedmineEntryGroupControl, '/redmine/xiake')


# 成本考量
from route.control.redmine.redmine_lirun_control import RedmineLirunProjectControl
api.add_resource(RedmineLirunProjectControl, '/redmine/project_lirun')


# 配置
from route.control.redmine.redmine_workday_control import RedmineWorkdayControl
api.add_resource(RedmineWorkdayControl, '/redmine/workday')

#  定时任务部分
class Config(object):
    SCHEDULER_API_ENABLED = True


scheduler = APScheduler()


@scheduler.task('cron', id='task1', day='*', hour='03', minute='00', second='00')
def task1():  # 每天凌晨3点跑一次
    # 先获取所有项目，看看有没有误差的
    from route.service.redmine.redmine_project_service import RedmineProjectService
    RedmineProjectService.update_from_redmine()
    # 再获取用户，看看有没有误差的
    from route.service.redmine.redmine_user_service import RedmineUserService
    RedmineUserService.update_from_redmine()
    # 再同步工时，看看有没有误差的
    from route.service.redmine.redmine_entry_service import RedmineEntryService
    RedmineEntryService.update_from_redmine()


@scheduler.task('cron', id='task2', day='*', hour='20', minute='00', second='00')
def task2():  # 每天晚上8点跑一次
    # 再同步工时，看看有没有误差的
    from route.service.redmine.redmine_entry_service import RedmineEntryService
    RedmineEntryService.update_xiake_from_redmine()


@scheduler.task('cron', id='task3', day='*', hour='13', minute='00', second='00')
def task3():  # 每天下午1点跑一次，看看谁的每日计划没有写
    # 首先先算出今天的日期，并且判定是不是工作日
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    from route.service.redmine.redmine_workday_service import RedmineWorkdayService
    if RedmineWorkdayService.is_workday(today):
        # 获取到所有侠客组的人员，并且得到他们当天的每日计划
        from route.service.routine.daily_service import DailyService
        from route.service.config.user_service import UserService
        from conf.custom_conf import ZUYUAN_ROLE_ID
        daily_list = DailyService.get_dailys_by_date(today)
        user_list = UserService.get_users_by_role_id(ZUYUAN_ROLE_ID)
        user_dict = {each.show_name: each for each in user_list}
        # 将每日计划符合要求的从user_list里面删除，剩下的人则是存在问题的
        for each_daily in daily_list:
            if each_daily.user.show_name in user_dict and len(each_daily.content.strip()) > 0:
                user_dict.pop(each_daily.user.show_name)
        from route.service.routine.score_record_service import ScoreRecordService
        from tools.utils.my_email import send_email
        for each_user in user_dict:
            res_score = ScoreRecordService.get_res_score_by_user_id(user_dict[each_user].id)
            ScoreRecordService.add_score_record(user_dict[each_user].id, "01", f"{today}未及时填写", -1, res_score.res_score - 1, "jingjian")
            send_email(f"{user_dict[each_user].login_name}@datagrand.com", f"{today}每日计划缺漏，扣除一分", f"{today}每日计划缺漏，扣除一分")
        from route.service.system.log_service import LogService
        LogService.add_log("0", "定时扣分任务", f"合计完成{len(user_dict)}名用户在{today}未及时填写每日计划从而扣分，分别为{','.join(user_dict.keys())}")



@scheduler.task('cron', id='task4', day='*', hour='21', minute='00', second='00')
def task4():  # 第一个休息日晚上9点跑一次，看看谁的redmine没有写
    pass   # 后面再写，逻辑和之前有点类似
    # today = datetime.datetime.now().strftime("%Y-%m-%d")
    # last_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    # from route.service.redmine.redmine_workday_service import RedmineWorkdayService
    # if RedmineWorkdayService.is_workday(last_day) and not RedmineWorkdayService.is_workday(today):
    #     # 如果昨天是工作日但是今天是休息日，则需要进行redmine统计
    #     from route.service.redmine.redmine_user_service import RedmineUserService
    #     user_list = RedmineUserService.get_xiake_user()
    #     from route.service.redmine.redmine_entry_service import RedmineEntryService
    #     RedmineEntryService.get_all_entry_of_xiake()

@app.route('/')
def index():
    return render_template('index.html')

from flask import jsonify
@app.route('/api/stock-data/<code>')
def get_stock_data(code):
    try:
        from route.service.stock_market.stock_service import StockService
        data = StockService.test(code)
        result = [{
            'date': item.trade_date,
            'open': item.open,
            'high': item.high,
            'low': item.low,
            'close': item.close,
            'volume': item.vol
        } for item in data]
        return jsonify(result)
    except Exception as e:
        # logger.error(f'获取股票数据失败: {str(e)}')
        print(traceback.format_exc())
        return jsonify({'error': '获取数据失败'}), 500

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
