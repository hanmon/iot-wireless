#!/usr/bin/python3

import serial
import time
import json
import configparser 
import RPi.GPIO as GPIO
from random import randint


config = configparser.ConfigParser()
config.read('../cht.conf')
projectKey = config.get('device-key', 'projectKey')
deviceId   = config.get('device-key', 'deviceId')
sensorId   = config.get('device-key', 'sensorId')


def init_serial(_port='/dev/ttyAMA0', _baudrate=9600):
    ser = serial.Serial(_port, _baudrate)

    if ser.isOpen() == False:
        ser.open()

    ser.bytesize = 8
    ser.parity   = "N"
    ser.stopbits = 1
    ser.timeout  = 5

    return ser



def power_on(_power_pin=7):
    print("Power On, please wait...")

    GPIO.setmode(GPIO.BOARD)  
    GPIO.setup(_power_pin, GPIO.OUT)    
    time.sleep(0.1)
    GPIO.output(_power_pin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(_power_pin, GPIO.LOW)
    time.sleep(5)



def power_down(_power_pin=7):
    print("Power Down, please wait...")

    GPIO.setmode(GPIO.BOARD)  
    GPIO.setup(_power_pin, GPIO.OUT)    
    time.sleep(0.1)
    GPIO.output(_power_pin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(_power_pin, GPIO.LOW)
    time.sleep(5)
    GPIO.cleanup()

    print("Power Down OK")



def send_n_recv(_cmd, _t=0.5):
    buff = ''
    ret = -1

    ser.write((_cmd + '\r\n').encode('utf-8'))
    time.sleep(_t)

    if ser.inWaiting():
        time.sleep(_t)
        buff = ser.read(ser.inWaiting())

    if buff != '':
        s = buff.decode('utf-8')
        print(s)
        ret = s.find("OK")

    return False if ret == -1 else True



def genEscapeJsonStr(json_dict):
    json_str = json.dumps(json_dict).replace(" ", "")
    str_len = len(json_str) + 2

    json_str = "[" + json_str.replace('"', '\\"') + "]"
    
    return (json_str, str_len)



if __name__ == '__main__':

    ser = init_serial()
    power_on()

    send_n_recv("AT")
    send_n_recv("ATE1")

    # Regist network
    send_n_recv("AT+CMNB=1")
    send_n_recv("AT+CPIN?")
    send_n_recv("AT+CSQ")
    send_n_recv("AT+CGREG?")
    send_n_recv("AT+CGNAPN")
    send_n_recv("AT+CPSI?")
    send_n_recv("AT+CGNAPN")


    # MQTT connect
    client_id = str(randint(1, 128))

    send_n_recv("AT+CNACT=0,1")
    send_n_recv('AT+SMCONF="CLIENTID",' + client_id)
    send_n_recv('AT+SMCONF="USERNAME","' + projectKey + '"')
    send_n_recv('AT+SMCONF="PASSWORD","' + projectKey + '"')
    send_n_recv('AT+SMCONF="CLEANSS",1')
    send_n_recv('AT+SMCONF="URL","iot.cht.com.tw","1883"')
    send_n_recv('AT+SMCONF="QOS",0')
    send_n_recv('AT+SMCONF="RETAIN",0')
    send_n_recv('AT+SMCONF="KEEPTIME",60')
    send_n_recv("AT+SMCONF?")
    send_n_recv("AT+SMCONN", _t=5)


    # MQTT pub
    jdict = {"id":sensorId, "value":[ client_id ]}
    escape_json_str, str_len = genEscapeJsonStr(jdict)

    send_n_recv('AT+SMPUB="/v1/device/' + deviceId + '/rawdata",' + str(str_len) + ',1,0', _t=0.5)

    time.sleep(3)
    print("========================")
    json_str = "[" + json.dumps(jdict).replace(" ", "") + "]"
    str_len = len(json_str)
    print(json_str)
    ser.write(json_str.encode('utf-8'))
    print("========================")
    time.sleep(5)

    ser.flush()
    ser.close()

    power_down()
