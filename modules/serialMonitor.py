#!/usr/bin/python
import serial
import os
import sys
import time
import atexit

class serialMonitor():
    def __init__(self, port='/dev/ttyUSB0', baudrate=8086):
        atexit.register(self.closePort)
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate)
        os.environ["PORT_OPEN"] = 'TRUE'

    def openPort(self):
        self.serial.open()
        os.environ["PORT_OPEN"] = 'TRUE'
        return True

    def closePort(self):
        self.serial.close()
        os.environ["PORT_OPEN"] = 'FALSE'
        return True

    def readline(self):
        if (self.serial.is_open):
            line = bytearray()
            while True:
                c = self.serial.read()
                if c:
                    line += c
                    if line[-2:] in ['\r\r', '\r\n']:
                        break
                else:
                    break
        self.data = bytes(line)
        self.writeSerialBuffer()
        return self.data

    def writeSerialBuffer(self):
        os.environ["SERIALBUFFER"] = self.data
        return True

    def readSerialBuffer(self):
        return os.environ["SERIALBUFFER"]

if __name__ == '__main__':
    if os.environ["PORT_OPEN"] == "TRUE":
        print('\n\n\n')
        print(os.environ["SERIALBUFFER"])
    else:
        ser = serialMonitor(port, baudrate).openPort()
        while True:
            print('\n\n\n')
            print(ser.readline())
            time.sleep(1)
