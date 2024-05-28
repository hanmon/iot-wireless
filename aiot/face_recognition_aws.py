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
regImage="registration.jpg"
recogImage="recognition.jpg"

camera = picamera.PiCamera()
camera.resolution = (320, 240)

time.sleep(2)    # Camera warm-up time

def play_audio_file(fname):
    os.system("aplay " + fname + " > /dev/null 2>&1")

def takePhoto(purpose="recognition"):
    if purpose=="registration":
        print("拍設註冊用照片中，請微笑 : )")
        camera.capture(regImage)
        img=cv2.imread(regImage)
        cv2.putText(img,"Registration Succeddeed!",(10, 40), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 255, 255), 1, cv2.LINE_AA) 
        cv2.imshow('Result', img)
        # 按下任意鍵則關閉所有視窗
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("拍設辨識照片中，請微笑 : )")
        camera.capture(recogImage)

def compare_faces(sourceFile, targetFile):

    client = boto3.client('rekognition')

    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')
    imgTarget = cv2.imread(targetFile)
    imgSource = cv2.imread(sourceFile)
    imgHeight, imgWidth, channels = imgTarget.shape
    print("src:{},target:{}".format(sourceFile,targetFile))
    try:
        response = client.compare_faces(SimilarityThreshold=80,SourceImage={'Bytes': imageSource.read()},TargetImage={'Bytes': imageTarget.read()})
        print(response)
        if response['FaceMatches'] not in (None, "", [], {}):
            for faceMatch in response['FaceMatches']:
                position = faceMatch['Face']['BoundingBox']
                similarity = str(faceMatch['Similarity'])
                print('The face at ' + str(position['Left']) + ' ' +
                    str(position['Top']) + ' matches with ' + similarity +
                    '% confidence')
                cv2.putText(imgTarget,"Verification Succeedded!",(10, 40), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 255, 255), 1, cv2.LINE_AA)    
                leftCorner=(int(position['Left']*imgWidth), int(position['Top']*imgHeight))
                rightCorner=(int(position['Left']*imgWidth+position['Width']*imgWidth), int(position['Top']*imgHeight+position['Height']*imgHeight))
                cv2.rectangle(imgTarget, leftCorner, rightCorner, (0, 255, 0), 2)
            ai_speak("驗證成功!")
        else:
            ai_speak("驗證失敗!")    
        #將Target與Source兩張圖併排顯示
        time.sleep(2)
        max_height = max(imgTarget.shape[0], imgSource.shape[0])
        resized_imageTarget = cv2.resize(imgTarget, (int(imgTarget.shape[1] * max_height / imgTarget.shape[0]), max_height))
        resized_imageSource = cv2.resize(imgSource, (int(imgSource.shape[1] * max_height / imgSource.shape[0]), max_height))
        numpy_horizontal = np.hstack((resized_imageTarget, resized_imageSource))
        cv2.imshow('Result', numpy_horizontal)
        # 按下任意鍵則關閉所有視窗
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        imageSource.close()
        imageTarget.close()
        return len(response['FaceMatches']),response
    
    except Exception as e:
        print("呼叫AWS API發生錯誤:{}".format(e))
        ai_speak("驗證失敗!")  
        return


def main():
    is_registering=False
    def on_detected(keyword):
        print("Button pressed")
        play_audio_file("resources/ding_half.wav")
        nonlocal is_registering
        if is_registering==True:
            #拍攝註冊照片
            takePhoto("registration") 
            is_registering=False
        else:
        # print('found {}'.format(keyword))
            takePhoto("recognition")
            face_matches,response=compare_faces(regImage,recogImage)
            if face_matches==1:
                print("驗證成功!")
            else:
                print("驗證失敗...")
            
        
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