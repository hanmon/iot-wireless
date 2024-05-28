#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2017, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# take_photo.py
# Capture an image to a file
#
# Author : sosorry
# Date   : 11/14/2014

import picamera
import time
import RPi.GPIO as GPIO
import os
import boto3
import cv2
import numpy as np
import sys
import pixels
from tts import ai_speak
#for detecting button push event
GPIO.setmode(GPIO.BOARD)
BTN_PIN = 11
GPIO.setup(BTN_PIN, GPIO.IN)
objImage="obj_detection.jpg"

camera = picamera.PiCamera()
camera.resolution = (320, 240)

time.sleep(2)    # Camera warm-up time

def play_audio_file(fname):
    os.system("aplay " + fname + " > /dev/null 2>&1")

def detect_labels_local_file(photo):
    client=boto3.client('rekognition')
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    print('偵測到此照片裡的物件：' + photo)    
    # for label in response['Labels'][:3]:
    #     print (label['Name'] + ' : ' + str(label['Confidence']))
    return response

def takePhoto(purpose="recognition"):
    if purpose=="registration":
        print("拍設註冊用照片中，請微笑 : )")
        camera.capture(objImage)
        img=cv2.imread(objImage)
        cv2.putText(img,"Registration Succeddeed!",(10, 40), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 255, 255), 1, cv2.LINE_AA) 
        cv2.imshow('Result', img)
        # 按下任意鍵則關閉所有視窗
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("拍設辨識照片中，請微笑 : )")
        camera.capture(objImage)

def object_detection(sourceFile):

    client = boto3.client('rekognition')

    imageSource = open(sourceFile, 'rb')
    # imageTarget = open(targetFile, 'rb')
    # imgTarget = cv2.imread(targetFile)
    imgSource = cv2.imread(sourceFile)
    imgHeight, imgWidth, channels = imgSource.shape
    try:
        response = detect_labels_local_file(sourceFile)
        resultStr0="Labels detected: " + str(len(response['Labels']))
        resultStr1=response['Labels'][0]['Name'] + ' : ' + str(response['Labels'][0]['Confidence'])
        resultStr2=response['Labels'][1]['Name'] + ' : ' + str(response['Labels'][1]['Confidence']) 
        resultStr3=response['Labels'][2]['Name'] + ' : ' + str(response['Labels'][2]['Confidence']) 
        print(response)   
        cv2.putText(imgSource,resultStr0, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,0.3,(0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(imgSource,"1st: "+ resultStr1, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,0.3,(0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(imgSource,"2nd: "+ resultStr2, (10,40), cv2.FONT_HERSHEY_SIMPLEX,0.3,(0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(imgSource,"3rd: "+ resultStr3,(10, 50), cv2.FONT_HERSHEY_SIMPLEX,0.3,(0, 255, 255), 1, cv2.LINE_AA)
        ai_speak("最有可能是"+response['Labels'][0]['Name'])
        cv2.imshow('Result', imgSource)
        print(resultStr1,resultStr2,resultStr3)
        # 按下任意鍵則關閉所有視窗
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    
    except Exception as e:
        print("呼叫AWS API發生錯誤:{}".format(e))
        ai_speak("驗證失敗!")  
        return


def main():
    def on_detected(keyword):
        print("Button pressed")
        play_audio_file("resources/ding_half.wav")
        takePhoto()
        response=object_detection(objImage)
        
    try:
        GPIO.add_event_detect(BTN_PIN, \
        GPIO.RISING, \
        callback=on_detected, \
        bouncetime=200)
        if len(sys.argv)>1 and sys.argv[1]=="r":
            is_registering=True
        while True:
            time.sleep(10)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()