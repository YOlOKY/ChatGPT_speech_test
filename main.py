#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date    : 2023-1-19
import wave
import requests
import time
from pyaudio import PyAudio, paInt16
from conf.config import *

import pygame
import re

from utils.asr_module import speech2text
from utils.tts_modeule import voice_play,answer2voice
from utils.weather_module import weather_run
from utils.chatGPT_module import answer_by_gpt
from datetime import datetime
import struct
import pyaudio
import pvporcupine
from conf.config import Picovoice_key,Picovoice_keyword_paths
import os


### 初始化
HOST = BaiDu_OpenApi_Url % (BaiDu_API_Key, BaiDu_Secret_Key)
os.environ["http_proxy"] = "http://127.0.0.1:7980"
os.environ["https_proxy"] = "http://127.0.0.1:7980"

framerate = 16000  # 采样率--树莓派设置参见readme中1.2
num_samples = 3000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
speech_file = 'voice_say/speech.wav'
# devpid = input('1536：普通话(简单英文),1537:普通话(有标点),1737:英语,1637:粤语,1837:四川话\n')
devpid = 1537

pa = pyaudio.PyAudio()

def getToken(host):
    res = requests.post(host)
    return res.json()['access_token']


def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()


def my_record():
    # pa = PyAudio()
    stream = pa.open(format=paInt16, channels=channels,
                     rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = []
    # count = 0
    t = time.time()
    print('正在录音...')

    while time.time() < t + 5:  # 秒
        string_audio_data = stream.read(num_samples, exception_on_overflow=False)  #内存溢出异常添加： exception_on_overflow=False
        my_buf.append(string_audio_data)
    print('录音结束.')
    save_wave_file('voice_say/speech.wav', my_buf)
    stream.close()


def getAudio(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data


def getQuery(TOKEN,FILEPATH):
    my_record()
    speech = getAudio(FILEPATH)
    query = speech2text(speech, TOKEN, int(devpid))
    print("query:", query)
    if type(query) != str:
        query = ""
    return query



def getAnswer(query):
    if len(query) >=2 :  #使用问答模型
        answer_by_gpt(query)
    else:
        answer = "你说什么？"  #兜底反问
        t=len(answer)*0.0001
        print(t)
        answer2voice(answer,file_name="./tts_voice/replay.mp3",sleep_time=t)


def main():
    TOKEN = getToken(HOST)  #获取百度token

    k = 0
    # porcupine = pvporcupine.create(keywords=['porcupine', 'ok google', "picovoice", "blueberry"])
    porcupine = pvporcupine.create(access_key=Picovoice_key,keyword_paths=Picovoice_keyword_paths)

    # pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length)

    hello_word = "AI小宝已启动，请说唤醒词！"  #欢迎词
    t = len(hello_word) * 0.01
    print(t)
    answer2voice(hello_word, file_name="./tts_voice/replay.mp3", sleep_time=t)


    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)

        ###　监测状态
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt_second = dt.split(":")[-1]
        if dt_second=="00":
            print(dt)

        if keyword_index >= 0:
            # Insert detection event callback here
            print("唤醒成功")

            flag = 1
            while flag == 1:
                # print('请输入数字选择语言：')

                ################################################## 启动录音提示  ##################################################
                voice_play(r"./voice_answer/叮零.mp3", 0.3)

                ############################################### 录音识别，转为文本  ##################################################
                query = getQuery(TOKEN, speech_file)  #
                query = re.sub(r'[\W]', '', query)  # 去标点符号

                ################################################## 一级回答策略 ##################################################
                if query in ["今天天气", "明天天气"]:
                    if query == "明天天气":
                        i = 1
                    else:
                        i = 0

                    ###执行天气播报
                    weather_run(i)

                elif query in ["音乐","歌曲","播放音乐","播放歌曲","给我唱个歌"]:
                    answer = "你是我的小呀小苹果，怎么爱你都不嫌多"  # 兜底反问
                    t = len(answer) * 0.08
                    print(t)
                    answer2voice(answer, file_name="./tts_voice/replay.mp3", sleep_time=t)

                elif query not in ["拜拜","退出","不用了"] :
                    ############################################# 二级回答策略
                    getAnswer(query)
                    flag = 1


                elif query in ["拜拜", "退出", "不用了"]:
                    answer = "哎呀，我得休息下"  # 兜底反问
                    t = len(answer) * 0.08
                    print(t)
                    answer2voice(answer, file_name="./tts_voice/replay.mp3", sleep_time=t)
                    break

                # time.sleep(3)
                print("####################################################", )

                k += 1
                if k % 4 == 0:  # 每N轮询问一次是否继续
                    # 启动提示
                    voice_play(r'voice_broadcast/if_continue.mp3', 1.5)

                    # 录音启动提示
                    voice_play(r"./voice_answer/叮零.mp3", 0.3)

                    result = getQuery(TOKEN, speech_file)
                    print(result)

                    yes_word = re.findall(r"[继续|是的]", result)
                    yes_len = len(yes_word)
                    if yes_len >= 1:
                        flag = 1
                    else:
                        flag = 0
                        pygame.mixer.music.stop()
                        pygame.quit()


if __name__ == '__main__':

    main()
