#!/usr/bin/env python
# coding=utf-8
# author: uncleyiba@qq.com
# datetime:2021-01-13 14:30
import os, sys, re, json, traceback, time
from flask_restful import Resource
from flask import jsonify, render_template, request, make_response
import _locale



_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])


class BaseControl(Resource):
    # def return_error(self, message, status_code):
    #     response = jsonify({"message": message})
    #     response.status_code = status_code
    #     return response

    def headers(self):
        return {'Content-Type': 'text/html'}



    def return_error(self, message, status_code):
        response = make_response(render_template("error.html", message=message), status_code, self.headers())
        return response


if __name__ == "__main__":
    pass
