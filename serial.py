#!/usr/bin/python
import serial

global ser
ser = serial.Serial('/dev/ttyUSB0', 9600)

def readline(eol=b'\r\r'):
    leneol = len(eol)
    line = bytearray()
    while True:
        c = ser.read(1)
        if c:
            line += c
            if line[-leneol:] == eol:
                break
        else:
            break
    return bytes(line)

def main():
    while True:
        print  '\n\n\n'
        data = readline(b'\r\n\r\n').replace('\r\n', '').replace('\r', ' ')[:-1]
        print data

main()