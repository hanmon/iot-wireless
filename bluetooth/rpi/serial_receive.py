#!/usr/bin/python3

import serial
import time

port = serial.Serial("/dev/rfcomm0", baudrate=38400, timeout=0.5)

def main():
    while True:
        try:
            recvS = port.readlines()
            for recv in recvS:
                print("Arduino] " + recv.decode('utf-8'))
            time.sleep(0.1)
        except KeyboardInterrupt:
            port.flush()
            port.close()
            exit()

if __name__ == '__main__':
    main()
