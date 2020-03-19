#!/usr/bin/python
import serial
import os
import sys
import time
import atexit

BUFFER_FILE = "/var/lib/hymera/buffer"
STATUS_FILE = "/var/lib/hymera/status"

class serialMonitor():
	def __init__(self, port='/dev/ttyUSB0', baudrate=8086,status="1"):
		atexit.register(self.closePort)
		self.port = port
		self.baudrate = baudrate
		self.serial = serial.Serial(port=self.port, baudrate=self.baudrate)
		self.status = status
		self.openPort()

	def openPort(self):
		if not self.serial.is_open:
			self.serial.open()
		with open(STATUS_FILE, "w") as f:
			f.write(self.status)
		return True

	def closePort(self):
		self.serial.close()
		with open(STATUS_FILE, "w") as f:
			pass
		return True

	def readline(self):
		if (self.serial.is_open):
			line = bytearray()
			while True:
				c = self.serial.read()
				if c:
					line += c
					if line[-4:] == b'\r\n\r\n':
						break
				else:
					break
		self.data = bytes(line).replace(b"\r\n\r\n", b"").replace(b"\r", b" ")
		self.data = self.data.decode("utf-8")
		self.writeSerialBuffer()
		return self.data

	def writeSerialBuffer(self):
		with open(BUFFER_FILE, "w") as b:
			b.write(self.data)
		return True

	@staticmethod
	def readSerialBuffer():
		with open(BUFFER_FILE) as b:
			return b.readline()

	@staticmethod
	def isInUse():
		with open(STATUS_FILE) as f:
			return f.read(1)

	@staticmethod
	def continousRead():
		while True:
			print("\n\n\n")
			print(serialMonitor.readSerialBuffer())
			time.sleep(1)

if __name__ == '__main__':
	if serialMonitor.isInUse():
		while True:
			print("\n\n\n")
			print(serialMonitor.readSerialBuffer())
			time.sleep(1)
	else:
		ser = serialMonitor("/dev/ttyUSB0", 9600)
		try:
			ser.readline()
		except:
			pass
		while True:
			print('\n\n\n')
			print(ser.readline())
			time.sleep(1)
