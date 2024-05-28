#!/usr/bin/python3
# python3 nlu_play_music_aec.py 0.95
# alsactl --file ~/.config/asound.state restore
# alsactl --file ~/.config/asound.state store

import uuid
import os
import sys
import signal
import speech_recognition as sr
import urllib
import uuid
import json
import requests
import time    
import RPi.GPIO as GPIO
import subprocess
import configparser
import os
# from gtts import gTTS
from pygame import mixer
import tempfile
# import hue_clz
# import mod_plc_clz
import pixels
import threading

from voice_engine.source import Source
from voice_engine.ec import EC
from voice_engine.kws import KWS
# from iot_stt_mod import run,record
# from func_tts_pc import speak

#import openai related packages and varables
from openai import OpenAI
import wave
import pyaudio
import configparser 
config = configparser.ConfigParser()
config.read('../openai.conf')
openai_key = config.get('openai_key', 'key')
client = OpenAI(api_key=openai_key)
is_space_key_pressed=False
# 設定錄音參數
FORMAT = pyaudio.paInt16
CHANNELS = 1  # 聲道數
RATE = 44100  # 取樣率
CHUNK = 1024  # 緩衝區大小
RECORD_SECONDS = 5  # 錄製時間
WAVE_OUTPUT_FILENAME = "in.wav"  # 输出文件名
audio = pyaudio.PyAudio()
trimmed_ai_msg=""

interrupted = False

config = configparser.ConfigParser()
#config.read('smart_speaker.conf')
#config.read('mod_smart_speaker.conf')
# config.read(os.path.join(os.path.dirname(__file__),'mod_smart_speaker.conf'))
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.get('dialogflow', 'google_app_credential')
# project_id = config.get('dialogflow', 'project_id')
# session_id = str(uuid.uuid4())
# language_code = 'zh-TW'

#for detecting button push event
GPIO.setmode(GPIO.BOARD)
BTN_PIN = 11
GPIO.setup(BTN_PIN, GPIO.IN)

#for led displaying
pixel = pixels.Pixels()
def led_on():
    # pixel = pixels.Pixels()
    pixel.wakeup()
    time.sleep(3)


def led_off():
    # pixel = pixels.Pixels()
    pixel.off()
    time.sleep(1)

def led_think():
    # pixel = pixels.Pixels()
    pixel.think()
    time.sleep(1)

def led_speak():
    # pixel = pixels.Pixels()
    pixel.speak()
    time.sleep(1)


def audioRecorderCallback():

    global is_space_key_pressed
    is_space_key_pressed=False
    t = threading.Thread(target=led_on, args=())
    t.start()
    print("正在錄製，請講出你想說的話後，再次按下空白鍵以結束錄製")
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []
    # 录制音频
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)
    chunk_count=0
    while not is_space_key_pressed and chunk_count<int(RATE / CHUNK * RECORD_SECONDS):  
        data = stream.read(CHUNK)
        frames.append(data)  
        chunk_count=chunk_count+1                    
        pass
    is_space_key_pressed=False
    print("Finished recording.")
    # 停止錄音
    stream.stop_stream()
    stream.close()

    led_off()
    print("converting audio to text")

    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    audio_file= open("./in.wav", "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    messages=[]
    print(f'me>')
    print(transcript.text)
    api_input_text="請在80個字的限制內回覆以下問題。Please reply to the following question within a limit of 80 words, ensuring the response contains no sentence breaks." + transcript.text
    print("api_input_text:{}".format(api_input_text))
    messages.append({"role":"user","content":api_input_text})   # 添加 user 回應

    led_think()
    response = client.chat.completions.create(model="gpt-4-1106-preview",
    max_tokens=300,
    temperature=0.5,
    messages=messages)
    print(response.choices[0])
    original_ai_msg = response.choices[0].message.content.replace('\n','')

    print(f'ai > {original_ai_msg}')
    led_off()
    speech_file_path = "speech.wav"
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=original_ai_msg
    )

    result=response.stream_to_file(speech_file_path)
    encoded_text = original_ai_msg.encode('utf-8')
    #speak(encoded_text)
    led_speak()
    result=os.system("mpg123 {} > /dev/null 2>&1".format(speech_file_path))
    # play_audio_file(speech_file_path)
    if result==0:
        print("執行成功")
        #play_audio_file(speech_file_path)
    else:
        print("播放失敗")
    led_off()


def play_audio_file(fname):
    os.system("aplay " + fname + " > /dev/null 2>&1")

def main():
    os.system("alsactl --file ~/.config/asound.bee restore")
    src = Source(rate=16000, channels=1, frames_size=1600)
    ec = EC(channels=src.channels, capture=0, playback=2) 

    def on_detected(keyword):
        print("Button pressed")
        global is_space_key_pressed
        is_space_key_pressed=True
        print('found {}'.format(keyword))
        play_audio_file("resources/ding_half.wav")

        try:
            subprocess.call("kill -9 `ps aux | grep python3 | grep yt3.py | awk '{print $2}'`", shell=True)
        finally:
            audioRecorderCallback()
            
    def mycallback(channel):
            print("Button pressed")
    try:
        GPIO.add_event_detect(BTN_PIN, \
        GPIO.RISING, \
        callback=on_detected, \
        bouncetime=200)
        while True:
            time.sleep(10)
    finally:
        GPIO.cleanup()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            led_off()

            break


if __name__ == '__main__':
    main()
