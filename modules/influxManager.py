#!/usr/bin/python3
import time
import os
import sys
from datetime import datetime
from influxdb import InfluxDBClient

class influxManager():
	def __init__(self, database, measurement, host='localhost', port=8086):
		self.client = InfluxDBClient(host='localhost', port=8086)
		self.client.switch_database(database)
		self.database = database
		self.measurement = measurement

	def write_points(self, json):
		self.client.write_points([{'fields': json, 'measurement': self.measurement, 'time': datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%SZ")}])
		return True