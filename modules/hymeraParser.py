#!/usr/bin/python3
import sys
import os
import time

class hymeraParser():
    def __init__(self):
        self.raw_data = ""
        self.power, self.temperature, self.current, self.voltage = 0

    def parse(self, data):
        self.raw_data = ""
        self.split_data = self.raw_data.split(" ")
        self.temperature = self.split_data[2]
        self.voltage = self.split_data[0]
        self.current = self.split_data[1]
        current = [i for i in self.split_data if "A" in i][2]
        voltages = [i for i in self.split_data if "V" in i]
        if len(voltages) in [5,6]:
            voltage = voltages[2]
        elif len(voltages) == 7:
            voltage = voltages[6]
        self.power = float(current.replace("A", "")) * float(voltage.replace("V", ""))
        csv = ",".join(self.split_data)
        self.json = {"csv": csv, "data": {"STACK_V": self.voltage, "STACK_I": self.current, "OUTPUT_POWER": self.power, "STACK_TEMP": self.temperature}}
        return self.json
