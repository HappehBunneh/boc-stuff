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

if __name__ == "__main__":
    testStr = "18.57V 00.0A 011.6C 009.8C 13.03V 0000A 1B 0B 0000 00.0C 3328 00.09V 00.0A 3998 25.20V 28.00V 0001m 0001m 0119 042d 28.00V 0000 00.00V 0000 2014/04/15 06:16:12 3106 01 1975 001 00000413 00 7200"
    parser = hymeraParser()
    data = parser.parse(testStr)
    print(data["data"])
    print(data["csv"])
