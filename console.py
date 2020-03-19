#!/usr/bin/python3
import os
from modules.csvWriter import csvWriter
from modules.serialMonitor import serialMonitor
from modules.influxManager import influxManager
from modules.hymeraParser import hymeraParser
from datetime import datetime
from modules.grafanaDashboard import grafanaApi
import atexit
import psutil

STATUS_FILE = "/var/lib/hymera/status"
BUFFER_FILE = "/var/lib/hymera/buffer"
PID_FILE = "/var/lib/hymera/PID"

class Console():
	def __init__(self, serialNumber, model, testReason):
		now = datetime.now()
		self.fileName = model+"_"+serialNumber+"_"+testReason.replace(" ", "_")+"_"+now.strftime("%m~%d~%Y_%H:%M:%S")
		self.fileWriter = csvWriter(self.fileName)
		self.serialMonitor = serialMonitor("/dev/ttyUSB0", 9600, self.fileName)
		self.influx = influxManager("hymera", self.fileName)
		self.parser = hymeraParser()
		atexit.register(self.close)
		self.writePID()

	def close(self):
		self.clearPID()
		exit()

	def run(self):
		grafanaApi.createDashboard()
		try:
				self.serialMonitor.readline()
		except:
				pass
		while True:
			data = self.serialMonitor.readline()
			print("\n\n\n", data)
			parsedJson = self.parser.parse(data)
			self.fileWriter.writeToFile(parsedJson["csv"])
			self.influx.write_points(parsedJson["data"])

	def writePID(self):
		with open(PID_FILE, "w") as file:
			file.write(str(os.getpid()))

	@staticmethod
	def clearPID():
		with open(PID_FILE, "w") as file:
			pass

	@staticmethod
	def isSerialRunning():
		with open(STATUS_FILE) as file:
			if file.read() == "1":
				return True
			else:
				return False

	@staticmethod
	def isConsoleRunning():
		 with open(STATUS_FILE) as file:
			 if len(file.read()) > 1 and file.read(1) != "1":
				 return True
			 else:
				 return False

	@staticmethod
	def killSelf():
		with open(PID_FILE) as file:
			psutil.Process(int(file.read())).terminate()
		Console.clearPID()
		with open(STATUS_FILE, "w") as file:
			pass

if __name__ == "__main__":
	if Console.isSerialRunning():
		term = input("There is currently a serial monitor process running and no console process, create one? ")
		if term.lower()[0] == "y":
			 Console.killSelf()
		else:
			 serialMonitor.continousRead()
	if Console.isConsoleRunning():
		term = input("There is currently a console running, terminate the process? ")
		if term.lower()[0] == "y":
			 Console.killSelf()
		else:
			 serialMonitor.continousRead()
	model = input("Specify model type: ")
	serialNumber = input("Specify serial number: ")
	testReason = input("Purpose of test: ")
	app = Console(serialNumber, model, testReason)
	app.run()