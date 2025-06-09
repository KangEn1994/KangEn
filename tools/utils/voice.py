#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time          : 2025/06/10 02:46
# @Author        : kang_en
# @Email         : kang_en@vip.qq.com
# @File          : voice.py
import os, sys, datetime, re, json
import torch


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