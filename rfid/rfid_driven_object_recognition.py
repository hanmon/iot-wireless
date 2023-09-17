#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

try:
    while True:
        print("等待讀取HF RFID卡片")
        id, text = reader.read()
        print("卡號：{}".format(id))
        #print(text)
except KeyboardInterrupt:
    print("\r\nCtrl+C鍵盤中斷")
except Exception as e:
    print("某種原因造成RFID讀取失敗!")
finally:
    GPIO.cleanup()



