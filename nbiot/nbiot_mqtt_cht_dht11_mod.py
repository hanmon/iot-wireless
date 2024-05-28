#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time,json
import configparser 
import adafruit_dht
import board
from random import randint
config = configparser.ConfigParser()
config.read('../cht.conf')
projectKey = config.get('device-key', 'projectKey')
deviceId   = config.get('device-key', 'deviceId')
sensorId   = config.get('device-key', 'sensorId')
dht11Id    = config.get('device-key', 'dht11Id')

dhtDevice = adafruit_dht.DHT11(board.D18)

ser = serial.Serial('/dev/ttyAMA0',9600)
ser.flushInput()

powerKey = 4
rec_buff = ''

def powerOn(powerKey):
	print('SIM7070X is starting:')
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(powerKey,GPIO.OUT)
	time.sleep(0.1)
	GPIO.output(powerKey,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(powerKey,GPIO.LOW)
	time.sleep(5)
	ser.flushInput()
	print('SIM7070X is ready')

def powerDown(powerKey):
	print('SIM7070X is loging off:')
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(powerKey,GPIO.OUT)
	GPIO.output(powerKey,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(powerKey,GPIO.LOW)
	time.sleep(5)
	print('Good bye')
	
def sendAt(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(timeout)
	if ser.inWaiting():
		time.sleep(0.1 )
		rec_buff = ser.read(ser.inWaiting())
	if rec_buff != '':
		if back not in rec_buff.decode():
			print(command + ' back:\t' + rec_buff.decode())
			return 0
		else:
			print(rec_buff.decode())
			return 1
	else:
		print(command + ' no responce')

def checkStart():
    while True:
        # simcom module uart may be fool,so it is better to send much times when it starts.
        ser.write( 'AT\r\n'.encode() )
        time.sleep(1)
        ser.write( 'AT\r\n'.encode() )
        time.sleep(1)
        ser.write( 'AT\r\n'.encode() )
        time.sleep(1)
        if ser.inWaiting():
            time.sleep(0.01)
            recBuff = ser.read(ser.inWaiting())
            print('SOM7080X is ready\r\n')
            print( 'try to start\r\n' + recBuff.decode() )
            if 'OK' in recBuff.decode():
                recBuff = ''
                break 
        else:
            powerOn(powerKey)


try:
    checkStart()
    sendAt('AT+CMNB=1','OK',1)
    time.sleep(1)
    print('wait for signal')
    time.sleep(10)
    sendAt('AT+CSQ','OK',1)
    time.sleep(1)
    sendAt('AT+CPSI?','OK',1)
    time.sleep(1)
    sendAt('AT+CGREG?','+CGREG: 0,1',0.5)
    time.sleep(1)
    sendAt('AT+CNACT=0,1','OK',1)
    time.sleep(1)
    sendAt('AT+CACID=0', 'OK',1)
    time.sleep(1)
    sendAt('AT+SMCONF=\"URL\",iot.cht.com.tw,1883','OK',1)
    time.sleep(1)
    sendAt('AT+SMCONF=\"USERNAME\",\"'+projectKey+'\"','OK',1)
    time.sleep(1)
    sendAt('AT+SMCONF=\"PASSWORD\",\"'+projectKey+'\"','OK',1)
    time.sleep(1)
    sendAt('AT+SMCONF=\"KEEPTIME\",60','OK',1)
    time.sleep(1)
    sendAt('AT+SMCONN','OK',5)
    time.sleep(1)
    #sendAt('AT+SMSUB=\"waveshare_pub\",1','OK',1)
    client_id = str(randint(0, 65535))

    while 1:
        try:
            # humd=randint(50, 65)
            # temp=randint(20,35)
            humd = str(dhtDevice.humidity)
            temp = str(dhtDevice.temperature)
            json_doc = [{"id":dht11Id, "value":[ humd,temp ]}]
            # escape_json_str, str_len = genEscapeJsonStr(jdict)
            json_payload=json.dumps(json_doc)
            str_len=len(json_payload)
            print('AT+SMPUB=\"/v1/device/' + deviceId + '/rawdata\",' + str(str_len) +',0,0')
            sendAt('AT+SMPUB=\"/v1/device/' + deviceId + '/rawdata\",' + str(str_len) +',0,0','OK',1)
            time.sleep(1)
            print(json_payload)
            ser.write(json_payload.encode())
            time.sleep(10);
            print('send message successfully!')
            # sendAt('AT+SMDISC','OK',1)
            # sendAt('AT+CNACT=0,0', 'OK', 1)
            # powerDown(powerKey)
        except:
            pass
        

except Exception as e:
    print("An exception occurred:", str(e))
    if ser != None:
        ser.close()
    sendAt('AT+SMDISC','OK',1)
    sendAt('AT+CNACT=0,0', 'OK', 1)
    powerDown(powerKey)
    GPIO.cleanup()