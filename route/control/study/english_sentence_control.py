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
from route.service.feishu_service import FeishuService
import torch

# 配置你的飞书表格token、sheet_id和区域
EXCEL_TOKEN = "QUqcsupWSh3i78tzEAtcy2k7nYM"
SHEET_ID = "1MJzYJ"


class EnglishSentenceControl(BaseControl):
    def get(self):
        # 获取到指定飞书文档中的数据量，假设最多10000行
        start, end = 2, 10000
        while start < end:
            mid = (start + end) // 2
            area = f"B{mid}:C{mid}"
            values = FeishuService.read_feishu_excel_sheet(EXCEL_TOKEN, SHEET_ID, area)
            # print(values)
            if values[0][0] and len(values[0][0]) > 0:
                start = mid + 1
            else:
                end = mid
        row_count = start - 1 
        return render_template('study/english_sentence.html', row_count=row_count)

    def post(self):
        # 获取一个随机的数字，并且飞书文档中返回那一行的数据
        row_count = request.form.get("row_count", None)
        random_num = random.randint(2, int(row_count))
        area = f"B{random_num}:C{random_num}"
        # 获取到飞书文档中对应随机数行的数据
        values = FeishuService.read_feishu_excel_sheet(EXCEL_TOKEN, SHEET_ID, area)
        # print(values)
        e, c = values[0][0], values[0][1]
        # tts = gTTS(text=e, lang="en", slow=False)
        # tts.save(f"doc/{random_num}.mp3")
        text_to_speech_silero(e, file_path=f"doc/{random_num}.wav", speaker="en_0")
        # 返回结果
        return {"english": e, "chinese": c, "path": f"doc/{random_num}.wav"}



def text_to_speech_silero(text, file_path="test/output.wav", speaker="en_0"):
    """
    Silero TTS - 轻量级神经网络方案
    参数：
        speaker: 音色选择 (en_0, en_1, ... en_117)，默认为en_99女性声音
    """
    # 本地模型路径（需先下载）
    model_path = "doc/v3_en.pt"  
    # 加载模型
    device = torch.device('cpu')
    model = torch.package.PackageImporter(model_path).load_pickle("tts_models", "model")
    model.to(device)
    
    # 生成语音
    sample_rate = 48000
    model.save_wav(
        text=text,
        speaker=speaker,
        sample_rate=sample_rate,
        audio_path=file_path
    )