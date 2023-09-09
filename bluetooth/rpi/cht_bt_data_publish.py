#!/usr/bin/python3

import paho.mqtt.client as mqtt
import numpy as np
import time
import json
import random
import configparser 
import serial
port = serial.Serial("/dev/rfcomm0", baudrate=38400, timeout=0.5)
config = configparser.ConfigParser()
config.read('../cht.conf')
projectKey = config.get('device-key', 'projectKey')
deviceId   = config.get('device-key', 'deviceId')
dht11Id   = config.get('device-key', 'dht11Id')

host = "iot.cht.com.tw"

topic = '/v1/device/' + deviceId + '/rawdata'
print(topic)

user, password = projectKey, projectKey

client = mqtt.Client()
client.username_pw_set(user, password)
client.connect(host, 1883, 60)

# for i in range(100):
#     bpm = int(np.random.random()*100)
#     t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))

#     payload = [{"id":sensorId,"value":[bpm], "time":t}]
#     print(payload)
#     client.publish(topic, "%s" % ( json.dumps(payload) ))
#     time.sleep(3)

def MqttPub(temp,humid):
    t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))
    payload = [{"id":dht11Id,"value":[temp,humid], "time":t}]
    print(payload)
    client.publish(topic, "%s" % ( json.dumps(payload) ))

def main():
    while True:
        try:
            recvS = port.readlines()
            for recv in recvS:
                fields=recv.decode().split(',')
                print("Arduino] " + recv.decode('utf-8'))
                temp,humid=fields[1],fields[2]
                print("temp={},humid={}".format(temp,humid))
                MqttPub(temp,humid)
            time.sleep(0.1)
        except KeyboardInterrupt:
            port.flush()
            port.close()
            exit()

if __name__ == '__main__':
    main()