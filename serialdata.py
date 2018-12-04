#!/usr/bin/python
import serial

global ser
ser = serial.Serial('/dev/ttyUSB0', 9600)

def readline():
    line = bytearray()
    while True:
        c = ser.read()
        if c:
            line += c
            if line[-2:] in ['\r\r', '\r\n']:
                break
        else:
            break
    return bytes(line)

def main():
    while True:
        print  '\n\n\n'
        data = readline().replace('\r\n', '').replace('\r\r', '').replace('\r', ' ')[:-1]
        print data

main()