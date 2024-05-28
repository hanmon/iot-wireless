#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2019, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# take_photo.py
# Capture an image to a file
#
# Author : sosorry
# Date   : 2014/11/14

import picamera
import time
import cv2

camera = picamera.PiCamera()
camera.resolution = (320, 240)
time.sleep(2)    # Camera warm-up time
camera.capture('new.jpg')
time.sleep(2)
img = cv2.imread('new.jpg')
cv2.imshow('photo', img)
cv2.waitKey(0)
cv2.destroyAllWindows()