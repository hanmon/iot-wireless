#!/usr/bin/env python

import RPi.GPIO as GPIO
import cv2
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

def takePhoto(cam_exists=False,filename="12345678"):
    if cam_exists: 
        print("請微笑 : )")
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        file_path="/rekognition/"+ filename + ".png"
        cv2.imwrite(file_path, image)
    else:
        print("請安裝照相機後再試一次")

try:
    while True:
        print("等待讀取HF RFID卡片")
        id, text = reader.read()
        print("卡號：{}".format(id))
        print("拍攝註冊用照片")
        takePhoto(filename=str(id))
        #print(text)
except KeyboardInterrupt:
    print("\r\nCtrl+C鍵盤中斷")
except Exception as e:
    print("某種原因造成RFID讀取失敗!")
finally:
    GPIO.cleanup()



