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
		if not (self.serial.is_open):
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
				c = self.serial.read(1)
				if c:
					line += c
					if line[-4:] ==  b'\r\n\r\n':
						break
				else:
					break
		self.data = bytes(line).replace(b"\r\n\r\n", b"").replace(b"\r", b" ")
		self.data = self.data.decode("utf-8")
		self.writeSerialBuffer()
		return self.data

	def writeSerialBuffer(self):
		os.environ["SERIALBUFFER"] = self.data
		return True

	def readSerialBuffer(self):
		return os.environ["SERIALBUFFER"]

if __name__ == '__main__':
	ser = serialMonitor("/dev/ttyUSB0", 9600)
	#Throw away first exception
	try:
		ser.readline()
	except:
		pass
	while True:
		print('\n\n\n')
		print(ser.readline())
		time.sleep(1)
