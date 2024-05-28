#!/usr/bin/python3

import pixels
import time

pixel = pixels.Pixels()

print("pixel.off()()\n")
pixel.off()
time.sleep(1)

print("pixel.wakeup()\n")
pixel.wakeup()
time.sleep(3)

print("pixel.think()\n")
pixel.think()
time.sleep(3)

print("pixel.speak()\n")
pixel.speak()
time.sleep(3)

pixel.off()
time.sleep(1)
