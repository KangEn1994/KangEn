import os, sys, json
import time
import datetime
import lark_oapi as lark
from lark_oapi.api.calendar.v4 import *
from lark_oapi.api.auth.v3 import *
from lark_oapi.api.sheets.v3 import *
import requests

from conf.conf import FEISHU_APP_ID, FEISHU_APP_SECRET

client = lark.Client.builder().app_id(FEISHU_APP_ID).app_secret(FEISHU_APP_SECRET).enable_set_token(True).build()


class FeishuService:

    @staticmethod
    def get_token():
        """
        获取飞书的token
        :return:
        """
        # 构造请求对象
        request: InternalTenantAccessTokenRequest = InternalTenantAccessTokenRequest.builder() \
            .request_body(InternalTenantAccessTokenRequestBody.builder()
                .app_id(FEISHU_APP_ID)
                .app_secret(FEISHU_APP_SECRET)
                .build()) \
            .build()

        # 发起请求
        response: InternalTenantAccessTokenResponse = client.auth.v3.tenant_access_token.internal(request)

        # 处理失败返回
        # if not response.success():
        #     lark.logger.error(
        #         f"client.auth.v3.tenant_access_token.internal failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        #     return

        # 处理业务结果
        # lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        return json.loads(response.raw.content)["tenant_access_token"]
    

    @staticmethod
    def transform_timestamp_to_date(timestamp):
        """
        将时间戳转换为日期
        :param timestamp:
        :return:
        """
        return datetime.datetime.fromtimestamp(int(timestamp)).strftime("%H:%M:%S")

    @staticmethod
    def get_calendar_list():
        """
        获取日历列表
        :return:
        """
        # 构造请求对象
        request: ListCalendarRequest = ListCalendarRequest.builder() \
            .page_size(500) \
            .build()

        # 发起请求
        option = lark.RequestOption.builder().user_access_token(FeishuService.get_token()).build()
        response: ListCalendarResponse = client.calendar.v4.calendar.list(request, option)


        # 处理业务结果
        # print(type(lark.JSON.marshal(response.data, indent=4)))
        # a = json.loads(lark.JSON.marshal(response.data, indent=4))
        # print(type(a))
        return json.loads(lark.JSON.marshal(response.data, indent=4))["calendar_list"]
        # return response.data


    @staticmethod
    def get_events_of_oneday(date_str):
        """
        获取某一天的日程
        :param date_str: 2025-05-10
        :return:
        """
        # date_string = "2025-05-10"
        calendar_id_list = [each["calendar_id"] for each in FeishuService.get_calendar_list()]
        date_start = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        date_end = date_start + datetime.timedelta(days=1)
        # print(date_start.timestamp(), date_end.timestamp())
        # print(time.time())
        event_list = []
        for calendar_id in calendar_id_list:
            # 构造请求对象
            request: ListCalendarEventRequest = ListCalendarEventRequest.builder() \
                .calendar_id(calendar_id) \
                .page_size(500) \
                .start_time(int(date_start.timestamp())) \
                .end_time(int(date_end.timestamp())) \
                .user_id_type("user_id") \
                .build()

            # 发起请求
            option = lark.RequestOption.builder().user_access_token(FeishuService.get_token()).build()
            response: ListCalendarEventResponse = client.calendar.v4.calendar_event.list(request, option)

            event_list2 = json.loads(lark.JSON.marshal(response.data, indent=4))["items"]
            for each in event_list2:
                event_list.append(dict(start=FeishuService.transform_timestamp_to_date(each["start_time"]["timestamp"]), end=FeishuService.transform_timestamp_to_date(each["end_time"]["timestamp"]), title=each["summary"]))

        event_list.sort(key=lambda x: x["start"])
        # 处理业务结果
        return event_list

    @staticmethod
    def read_feishu_excel(sheet_token):
        """
        读取飞书表格
        :param sheet_id:
        :return:
        """
        # 构造请求对象
        request: QuerySpreadsheetSheetRequest = QuerySpreadsheetSheetRequest.builder() \
            .spreadsheet_token("Iow7sNNEphp3WbtnbCscPqabcef") \
            .build()

        # 发起请求
        response: QuerySpreadsheetSheetResponse = client.sheets.v3.spreadsheet_sheet.query(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.sheets.v3.spreadsheet_sheet.query failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))



    @staticmethod
    def read_feishu_excel_sheet(excel_token, sheet_id, area):
        """
        读取飞书表格 指定表格 指定sheet页 指定区域（API方式）
        :param excel_token: 表格token
        :param sheet_id: sheet页id
        :param area: 区域，如"A1:B10"
        :return: 区域内的数据
        """
        access_token = FeishuService.get_token()
        url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{excel_token}/values/{sheet_id}!{area}"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if data.get("code") != 0:
            return None
        # 返回区域内的值
        return data["data"]["valueRange"]["values"]





