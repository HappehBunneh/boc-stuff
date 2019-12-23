#!/usr/bin/python3
import time
import os
import sys
from influxdb import InfluxDBClient

class influxManager():
    def __init__(self, database, measurement, host='localhost', port=8086):
        self.client = InfluxDBClient(host='localhost', port=8086)
        self.client.switch_database(database)
        os.environ["INFLUX_DATABASE"] = database
        os.environ["INFLUX_MEASUREMENT"] = measurement

    def write_points(self):
        self.client.write_points([{'fields': json, 'measurement': measurement}])
        return True
