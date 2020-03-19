#!/usr/bin/python3
import sys
import os
import time

class hymeraParser():
	def __init__(self):
		self.raw_data = ""
		self.power = self.temperature = self.current = self.voltage = 0

	def parse(self, data):
		self.raw_data = data
		self.split_data = [i for i in self.raw_data.split(" ") if len(i) != 0]
		v_c_p = []
		for i in range(len(self.split_data)-1):
			if self.split_data[i][-1] == "V" and self.split_data[i+1][-1] == "A":
				v_c_p.append([float(self.split_data[i].replace("V", "")), float(self.split_data[i+1].replace("A", ""))])
		self.stack_voltage = v_c_p[0][0]
		self.stack_current = v_c_p[0][1]
		self.stack_power = round(self.stack_voltage*self.stack_current, 1)
		self.output_power = round(v_c_p[2][0]*v_c_p[2][1], 1)
		self.stack_temp = float(self.split_data[2].replace("+", "").replace("C", ""))
		self.ambient_temp = float(self.split_data[3].replace("+", "").replace("C", ""))
		self.csv = ",".join(self.split_data)
		self.json = {
				"data":{
					"STACK_VOLTAGE":self.stack_voltage,
					"STACK_CURRENT":self.stack_current,
					"STACK_POWER":self.stack_power,
					"OUTPUT_POWER":self.output_power,
					"STACK_TEMP":self.stack_temp,
					"AMBIENT_TEMP":self.ambient_temp
				},
				"csv": self.csv}
		return self.json

if __name__ == "__main__":
	from serialMonitor import serialMonitor
	parser = hymeraParser()
	if serialMonitor.isInUse():
		while True:
			print("\n\n\n")
			data = serialMonitor.readSerialBuffer()
			print(data)
			print(parser.parse(data))
			time.sleep(1)
	else:
		ser = serialMonitor("/dev/ttyUSB0", 9600)
		try:
			ser.readline()
		except:
			pass
		while True:
			print("\n\n\n")
			data = ser.readline()
			print(data)
			print(parser.parse(data))
			time.sleep(1)
