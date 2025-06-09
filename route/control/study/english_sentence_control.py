#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time          : 2025/05/15 05:10
# @Author        : kang_en
# @Email         : kang_en@vip.qq.com
# @File          : english_sentence_control.py
import os, sys, datetime, re, json
import traceback, time, random

from flask import render_template, request, session, jsonify
from route.control.base_control import BaseControl
from route.service.feishu_service import FeishuService, SENTENCES
from tools.utils.voice import text_to_speech_silero

# 配置你的飞书表格token、sheet_id和区域
EXCEL_TOKEN = "QUqcsupWSh3i78tzEAtcy2k7nYM"
SHEET_ID = "1MJzYJ"


class EnglishSentenceControl(BaseControl):
    def get(self):
        # 获取到指定飞书文档中的数据量，假设最多10000行
        sentences = FeishuService.get_all_sentences(EXCEL_TOKEN, SHEET_ID)
        # start, end = 2, 10000
        # while start < end:
        #     mid = (start + end) // 2
        #     area = f"B{mid}:C{mid}"
        #     values = FeishuService.read_feishu_excel_sheet(EXCEL_TOKEN, SHEET_ID, area)
        #     # print(values)
        #     if values[0][0] and len(values[0][0]) > 0:
        #         start = mid + 1
        #     else:
        #         end = mid
        # row_count = start - 1 
        return render_template('study/english_sentence.html', row_count=len(sentences))

    def post(self):
        # 获取一个随机的数字，并且飞书文档中返回那一行的数据
        row_count = request.form.get("row_count", None)
        random_num = random.randint(0,int(row_count) - 1)
        e, c = SENTENCES[random_num]["sentence"], SENTENCES[random_num]["translation"]
        # area = f"B{random_num}:C{random_num}"
        # # 获取到飞书文档中对应随机数行的数据
        # values = FeishuService.read_feishu_excel_sheet(EXCEL_TOKEN, SHEET_ID, area)
        # print(values)
        # e, c = values[0][0], values[0][1]
        # tts = gTTS(text=e, lang="en", slow=False)
        # tts.save(f"doc/{random_num}.mp3")
        # 判断文件是否存在
        file_path = f"doc/{SENTENCES[random_num]['id']}.wav"
        if not os.path.exists(file_path):
            text_to_speech_silero(e, file_path=file_path, speaker="en_0")
        # 返回结果
        return {"english": e, "chinese": c, "path": file_path}



