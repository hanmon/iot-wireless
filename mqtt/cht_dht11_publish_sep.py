#!/usr/bin/python3

import paho.mqtt.client as mqtt
import numpy as np
import time
import json
import board
import adafruit_dht
import configparser 

config = configparser.ConfigParser()
config.read('../cht.conf')
projectKey = config.get('device-key', 'projectKey')
deviceId   = config.get('device-key', 'deviceId')
dht11Id    = config.get('device-key', 'dht11Id')

dhtDevice = adafruit_dht.DHT11(board.D18)

host = "iot.cht.com.tw"

topic = '/v1/device/' + deviceId + '/rawdata'
print(topic)

user, password = projectKey, projectKey

client = mqtt.Client()
client.username_pw_set(user, password)
client.connect(host, 1883, 60)

for i in range(100):
    try:
        # humd = str(dhtDevice.humidity)
        # temp = str(dhtDevice.temperature)
        humid= str(np.random.randint(60,70))
        temp= str(np.random.randint(20,30))
        t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))

        payload = [{"id":"humid","value":[humid], "time":t},{"id":"temp","value":[temp], "time":t}]
        print(payload)
        client.publish(topic, "%s" % ( json.dumps(payload) ))
    except Exception as e:
        print("發生錯誤:",e)
        pass
    
    time.sleep(3)

