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

def detect_ppe_labels_local_file(photo):
    client=boto3.client('rekognition')
    with open(photo, 'rb') as image:
        response = client.detect_protective_equipment(Image={'Bytes': image.read()}, 
        SummarizationAttributes={'MinConfidence':80, 'RequiredEquipmentTypes':['FACE_COVER', 'HAND_COVER', 'HEAD_COVER']})
    print('偵測到此照片裡的物件：' + photo)    
    return response

def takePhoto(purpose="recognition"):
    if purpose=="registration":
        print("拍攝註冊用照片中，請微笑 : )")
        camera.capture(objImage)
        img=cv2.imread(objImage)
        cv2.putText(img,"Registration Succeddeed!",(10, 40), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 255, 255), 1, cv2.LINE_AA) 
        cv2.imshow('Result', img)
        # 按下任意鍵則關閉所有視窗
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("拍攝辨識照片中，請微笑 : )")
        camera.capture(objImage)

def ppe_detection(sourceFile):

    client = boto3.client('rekognition')

    imageSource = open(sourceFile, 'rb')
    imgSource = cv2.imread(sourceFile)
    imgHeight, imgWidth, channels = imgSource.shape
    try:
        response = detect_ppe_labels_local_file(sourceFile)
        # print(response)
        ppe_items_count=0
        if response['Persons'] not in (None, "", [], {}):
            for person in response['Persons']:
            
                print('Person ID: ' + str(person['Id']))
                print ('Body Parts\n----------')
                body_parts = person['BodyParts']
                if len(body_parts) == 0:
                        print ('No body parts found')
                else:
                    for body_part in body_parts:
                        print('\t'+ body_part['Name'] + '\n\t\tConfidence: ' + str(body_part['Confidence']))
                        print('\n\t\tDetected PPE\n\t\t------------')
                        ppe_items = body_part['EquipmentDetections']
                        if len(ppe_items) ==0:
                            print ('\t\tNo PPE detected on ' + body_part['Name'])
                        else:    
                            for ppe_item in ppe_items:
                                if ppe_item['Type']=="FACE_COVER":
                                    ppe_items_count=ppe_items_count+1
                                    print('\t\t' + ppe_item['Type'] + '\n\t\t\tConfidence: ' + str(ppe_item['Confidence'])) 
                                    print('\t\tCovers body part: ' + str(ppe_item['CoversBodyPart']['Value']) + '\n\t\t\tConfidence: ' + str(ppe_item['CoversBodyPart']['Confidence']))
                                    print('\t\tBounding Box:')
                                    print ('\t\t\tTop: ' + str(ppe_item['BoundingBox']['Top']))
                                    print ('\t\t\tLeft: ' + str(ppe_item['BoundingBox']['Left']))
                                    print ('\t\t\tWidth: ' +  str(ppe_item['BoundingBox']['Width']))
                                    print ('\t\t\tHeight: ' +  str(ppe_item['BoundingBox']['Height']))
                                    print ('\t\t\tConfidence: ' + str(ppe_item['Confidence']))
                                    leftCorner=(int(ppe_item['BoundingBox']['Left']*imgWidth), int(ppe_item['BoundingBox']['Top']*imgHeight))
                                    rightCorner=(int(ppe_item['BoundingBox']['Left']*imgWidth+ppe_item['BoundingBox']['Width']*imgWidth), int(ppe_item['BoundingBox']['Top']*imgHeight+ppe_item['BoundingBox']['Height']*imgHeight))
                                    cv2.rectangle(imgSource, leftCorner, rightCorner, (0, 255, 0), 2)
            if ppe_items_count>0:
                ai_speak("有"+str(len(response['Persons']))+"個人，"+str(ppe_items_count)+"個人戴口罩")
            else:
                ai_speak("有"+str(len(response['Persons']))+"個人，沒有人戴口罩")
            time.sleep(2)
            cv2.imshow('Result', imgSource)
            # 按下任意鍵則關閉所有視窗
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        else:
            ai_speak("沒有偵測到人")
            cv2.imshow('Result', imgSource)
            # 按下任意鍵則關閉所有視窗
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return len(response['Persons']),ppe_items_count
        
    
    except Exception as e:
        print("呼叫AWS API發生錯誤:{}".format(e))
        ai_speak("驗證失敗!")  
        return


def main():
    def on_detected(keyword):
        print("Button pressed")
        play_audio_file("resources/ding_half.wav")
        takePhoto()
        response=ppe_detection(objImage)
        
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