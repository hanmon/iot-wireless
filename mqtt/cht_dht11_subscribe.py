#!/usr/bin/python3

import paho.mqtt.client as mqtt
import configparser 

config = configparser.ConfigParser()
config.read('../cht.conf')
projectKey = config.get('device-key', 'projectKey')
deviceId   = config.get('device-key', 'deviceId')
dht11Id    = config.get('device-key', 'dht11Id')

host = "iot.cht.com.tw"
topic = '/v1/device/' + deviceId + '/sensor/' + dht11Id + '/rawdata'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: {}".format(str(rc)))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print("topic: {}, message: {}".format(msg.topic, str(msg.payload)))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

user, password = projectKey, projectKey
client.username_pw_set(user, password)
client.connect(host, 1883, 60)

client.loop_forever()

