#!/usr/bin/python3
import sys
import os
import time
from serialMonitor import serialMonitor

class hymeraParser():
	def __init__(self):
		self.raw_data = ""
		self.power = self.temperature = self.current = self.voltage = 0

	def parse(self, data):
		self.raw_data = data
		self.split_data = [i for i in self.raw_data.split(" ") if len(i) != 0]
		voltage_current_pairs = []
		for i in range(len(self.split_data) - 1):
			if self.split_data[i][-1] == "V" and self.split_data[i+1][-1] == "A":
				voltage_current_pairs.append([float(self.split_data[i].replace("V", "")), float(self.split_data[i+1].replace("A", ""))])
		self.stack_voltage = voltage_current_pairs[0][0]
		self.stack_current = voltage_current_pairs[0][1]
		self.stack_power = round((self.stack_voltage*self.stack_current), 1)
		self.output_power = round((voltage_current_pairs[2][0]*voltage_current_pairs[2][1]), 1)
		self.stack_temperature = float(self.split_data[2].replace("+","").replace("C",""))
		self.ambient_temperature = float(self.split_data[3].replace("+","").replace("C",""))
		self.json = {
				"data":
					{
						"STACK_V": self.stack_voltage,
						"STACK_I": self.stack_current,
						"STACK_POWER": self.stack_power,
						"OUTPUT_POWER": self.output_power,
						"STACK_TEMP": self.stack_temperature,
						"AMBIENT_TEMP": self.ambient_temperature
					},
				"csv": ",".join(self.split_data)}
		return self.json

if __name__ == "__main__":
	ser = serialMonitor('/dev/ttyUSB0', 9600)
	parser = hymeraParser()
	try:
		ser.readline()
	except:
		pass
	while True:
		print("\n\n\n")
		data = ser.readline()
		parsed = parser.parse(data)
		print(data)
		print(parsed["data"])
		time.sleep(1)
