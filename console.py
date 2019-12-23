#!/usr/bin/python3
import os
from modules.csvWriter import csvWriter
from modules.serialMonitor import serialMonitor
from modules.influxManager import influxManager
from modules.hymeraParser import hymeraParser
from datetime import datetime
import atexit

class Console():
    def __init__(self, serialNumber, model, testReason):
        now = datetime.now()
        self.fileName = model+"_"+serialNumber+"_"+testReason.replace(" ", "_")+"_"+now.strftime("%m/%d/%Y_%H:%M:%S")
        self.fileWriter = csvWriter(self.fileName)
        self.serialMonitor = serialMonitor()
        self.influx = influxManager("test", self.fileName)
        self.parser.parse = hymeraParser()
        atexit.register(self.close)
        os.environ["CONSOLE_RUNNING"] = "TRUE"

    def close(self):
        os.environ["CONSOLE_RUNNING"] = "FALSE"
        exit()

    def run(self):
        self.serialMonitor.open()
        while True:
            data = self.serialMonitor.readline()
            print("\n\n\n", data)
            parsedJson = self.parser.parse(data)
            self.fileWriter.writeToFile(parsedJson["csv"])
            self.influx.write_points(parsedJson["data"])

if __name__ == "__main__":
    if "CONSOLE_RUNNING" in os.environ:
        if os.environ["CONSOLE_RUNNING"] == "TRUE":
            print("There is currently a process running...")
    model = input("Specify model type: ")
    serialNumber = input("Specify serial number: ")
    testReason = input("Purpose of test: ")
    app = Console(serialNumber, model, testReason)
    app.run()

