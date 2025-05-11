#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/11
import datetime
from route.service.database.sql_pool import SqlPool
from route.entity.stock_market.stock_daily import StockDaily
from tools.utils.simple_utils import get_uuid
import tushare as ts
from conf.conf import TUSHARE_TOKEN

class StockService:
    # @staticmethod
    # def get_stock_by_project_id(project_id):
    #     session = SqlPool.get_session()
    #     project_license_record_list = []
    #     if project_id:
    #         project_license_record_list = session.query(Stock).filter(Stock.project_id == project_id).all()
    #     else:
    #         project_license_record_list = session.query(Stock).all()
    #     _ = [each.project for each in project_license_record_list]
    #     session.close()
    #     return project_license_record_list
    #
    # @staticmethod
    # def get_stock_need_continue():
    #     # 得到当前时间并且进行时间判定
    #     # now_datetime = datetime.datetime.now()
    #     # target_datetime = now_datetime - datetime.timedelta(days=7)
    #     # target_date = target_datetime.strftime('%Y-%m-%d')
    #     session = SqlPool.get_session()
    #     project_license_record_list = session.query(Stock).filter(Stock.type == Stock.CONTINUE).order_by(Stock.end_date).limit(20).all()
    #     _ = [each.project for each in project_license_record_list]
    #     session.close()
    #     return project_license_record_list

    @staticmethod
    def add(ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount):
        # session = SqlPool.get_session()
        stock = StockDaily(id=get_uuid(), ts_code=ts_code, trade_date=trade_date, open=open, high=high, low=low, close=close, pre_close=pre_close, change=change, pct_chg=pct_chg, vol=vol, amount=amount,
                      create_by="1", update_by="1")
        return stock
        # session.add(stock)
        # session.commit()
        # session.close()

    # @staticmethod
    # def update(license_id, product_info, machine_code, start_date, end_date, type, username):
    #     session = SqlPool.get_session()
    #     now_user = session.query(User).filter(User.login_name == username).one()
    #     project_license_record = session.query(Stock).filter(Stock.id == license_id).one()
    #     project_license_record.product_info = product_info
    #     project_license_record.machine_code = machine_code
    #     project_license_record.start_date = start_date
    #     project_license_record.end_date = end_date
    #     project_license_record.type = type
    #     project_license_record.update_by = now_user.id
    #     project_license_record.update_time = datetime.datetime.now()
    #     session.commit()
    #     session.close()
    #
    # @staticmethod
    # def delete(project_license_record_id):
    #     try:
    #         session = SqlPool.get_session()
    #         session.query(Stock).filter(Stock.id == project_license_record_id).delete()
    #         session.commit()
    #         session.close()
    #         return True
    #     except:
    #         return False

    @staticmethod
    def get_qfq_data(code):
        """
                #     'date': item.trade_date,
        #     'open': item.open,
        #     'high': item.high,
        #     'low': item.low,
        #     'close': item.close,
        #     'volume': item.vol
        :param code:
        :return:
        """
        ts.set_token(TUSHARE_TOKEN)
        pro = ts.pro_api()
        day_str = datetime.datetime.now().strftime("%Y%m%d")
        df = ts.pro_bar(ts_code=code, adj='qfq', start_date='19900101', end_date=day_str)
        r = []
        line, col = df.shape
        for i in range(line):
            e = df.loc[i]
            r.insert(0, dict(date=e["trade_date"], open=e["open"], high=e["high"], low=e["low"], close=e["close"], volume=e["vol"]))
        return r

    @staticmethod
    def upload_data(trade_date):
        ts.set_token(TUSHARE_TOKEN)
        pro = ts.pro_api()
        now = datetime.datetime.strptime("20250219", "%Y%m%d")
        day = now - datetime.timedelta(days=0)
        day_str = day.strftime("%Y%m%d")
        df = pro.daily(**{
            "ts_code": "", "trade_date": day_str, "start_date": "", "end_date": "", "offset": "", "limit": ""
        }, fields=["ts_code", "trade_date", "open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol",
                   "amount"
                   ])
        df = df.fillna(0)
        row, col = df.shape
        print(f"{day_str}那天共有数据{row}条")
        s = []
        for j in range(row):
            e = df.loc[j]
            # stock = StockService.add(e["ts_code"], e["trade_date"], e["open"], e["high"], e["low"], e["close"], e["pre_close"], e["change"], e["pct_chg"], e["vol"], e["amount"])
            # print(dict(e))
            s.append(dict(e))
            if len(s) == 1000 or j + 1 == row:
                session = SqlPool.get_session()
                row_count = session.bulk_insert_mappings(StockDaily, s)
                # stock = Stock(id=get_uuid(), ts_code=ts_code, trade_date=trade_date, open=open, high=high, low=low,
                #               close=close, pre_close=pre_close, change=change, pct_chg=pct_chg, vol=vol, amount=amount,
                #               create_by="1", update_by="1")

                session.commit()
                session.close()
                s = []

    @staticmethod
    def get_daily_data(code):
        try:
            session = SqlPool.get_session()
            data = session.query(StockDaily).filter(StockDaily.ts_code == code).order_by(StockDaily.trade_date).all()
            # print(data)
            session.close()
            return data
        except:
            return False

if __name__ == "__main__":
    ts.set_token(TUSHARE_TOKEN)
    pro = ts.pro_api()
    day_str = datetime.datetime.now().strftime("%Y%m%d")
    df = ts.pro_bar(ts_code="688256.SH", adj='qfq', start_date='19900101', end_date=day_str)

    line, col = df.shape
    for i in range(10, line):
        e = df.loc[i]
        e2 = df.loc[i - 10]
        if e["pct_chg"] > 19:
            print(f"交易日{e['trade_date']}, 开盘价{e['open']}，收盘价{e['close']}，涨跌幅{e['pct_chg']}，10日后收盘价{e2['close']}")







