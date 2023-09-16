# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from digi.xbee.devices import XBeeDevice
import paho.mqtt.client as mqtt
import numpy as np
import time
import json
import random
import configparser 
import serial
config = configparser.ConfigParser()
config.read('../../cht.conf')
projectKey = config.get('device-key', 'projectKey')
deviceId   = config.get('device-key', 'deviceId')
dht11Id   = config.get('device-key', 'dht11Id')
host = "iot.cht.com.tw"

topic = '/v1/device/' + deviceId + '/rawdata'
user, password = projectKey, projectKey
client = mqtt.Client()
client.username_pw_set(user, password)
client.connect(host, 1883, 60)
# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyUSB0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

def MqttPub(temp,humid):
    t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))
    payload = [{"id":dht11Id,"value":[temp,humid], "time":t}]
    print(payload)
    client.publish(topic, "%s" % ( json.dumps(payload) ))

def main():
    print(" +-------------------------------------------------+")
    print(" | XBee Python Library Receive Data Polling Sample |")
    print(" +-------------------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        device.flush_queues()

        print("Waiting for data...\n")
        
        while True:
            xbee_message = device.read_data()
            if xbee_message is not None:
                print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                         xbee_message.data.decode()))
                fields=xbee_message.data.decode().split(',')
                temp,humid=fields[0],fields[1]
                print("temp={},humid={}".format(temp,humid))
                MqttPub(temp,humid)

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
