#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2022/2/11
import datetime
from flask import render_template, request, session, jsonify
from route.control.base_control import BaseControl
from route.service.stock_market.stock_service import StockService


class StockControl(BaseControl):
    def get(self):
        return render_template('stock/stock.html')

    def post(self, code):
        return jsonify(StockService.get_qfq_data(code))
        # data = StockService.get_daily_data(code)
        # result = [{
        #     'date': item.trade_date,
        #     'open': item.open,
        #     'high': item.high,
        #     'low': item.low,
        #     'close': item.close,
        #     'volume': item.vol
        # } for item in data]
        # return jsonify(result)





if __name__ == "__main__":
    date_obj = datetime.datetime.now()
    print(date_obj.year)
    print(date_obj.month)
    print(date_obj.day)

    date_obj = datetime.datetime.strptime("2023-01-02", "%Y-%m-%d")
    print(date_obj.strftime('%Y-%m-%d'))
    date_obj = datetime.datetime.strptime("2023-1-2", "%Y-%m-%d") + datetime.timedelta(days=1)
    print(date_obj.strftime('%Y-%m-%d'))