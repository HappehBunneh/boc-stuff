#!/usr/bin/python
import os
import subprocess
import time
cwd = os.getcwd()

print('INSTALLING INFLUX')
os.system('sudo apt-get update && sudo apt install apt-transport-https curl')
os.system('curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -')
os.system('echo "deb https://repos.influxdata.com/debian jessie stable" | sudo tee /etc/apt/sources.list.d/influxdb.list')
os.system('sudo apt-get update && sudo apt-get install influxdb -y')
print('INFLUX INSTALLED')
print('INSTALLING PYTHON DEPENDANCIES')
os.system('pip3 install psutil')
os.system('pip3 install influxdb')
print('PYTHON DEPENDANCIES INSTALLED')
print('STARTING INFLUXDB')
os.system('sudo systemctl unmask influxdb')
os.system('sudo systemctl enable influxdb')
print('WAITING....')
time.sleep(10)
print('CONFIGURING INFLUX')
from influxdb import InfluxDBClient
client = InfluxDBClient(host='localhost', port=8086)
client.create_database('test')
client.close()
print('INFLUX CONFIGURED')