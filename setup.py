#!/usr/bin/python
import os
import subprocess
import time
cwd = os.getcwd()

print 'INSTALLING INFLUX'
os.system('sudo apt-get update && sudo apt install apt-transport-https curl')
os.system('curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -')
os.system('echo "deb https://repos.influxdata.com/debian jessie stable" | sudo tee /etc/apt/sources.list.d/influxdb.list')
os.system('sudo apt-get update && sudo apt-get install influxdb -y')
print 'INFLUX INSTALLED'
print 'INSTALLING PYTHON DEPENDANCIES'
os.system('pip install pyyaml')
os.system('pip install psutil')
os.system('pip install flask')
os.system('sudo apt-get install python-pandas -y')
os.system('sudo apt-get install python-numpy -y')
os.system('sudo apt-get install python-influxdb -y')
os.system('mkdir data_dir')
print 'PYTHON DEPENDANCIES INSTALLED'
print 'STARTING INFLUXDB'
subprocess.Popen('sudo nohup influxd &', shell=True)
print 'WAITING....'
time.sleep(10)
print 'CONFIGURING INFLUX'
from influxdb import InfluxDBClient
client = InfluxDBClient(host='localhost', port=8086)
client.create_database('test')
client.close()
print 'INFLUX CONFIGURED'
print 'CREATING EXECUTABLES'
os.system('chmod +x '+cwd+'/displaydata.py')
os.system('chmod +x '+cwd+'/console.py')
os.system('chmod +x '+cwd+'/switch.py')
os.system('chmod +x '+cwd+'/webserver/server.py')
print 'EXECUTABLES CREATED'
print 'CREATING SYMLINKS'
os.system('sudo ln -s '+cwd+'/webserver/server.py /usr/bin/server.py')
os.system('sudo ln -s '+cwd+'/switch.py /usr/bin/hym_on.py')
os.system('sudo ln -s '+cwd+'/console.py /usr/bin/hym_mon.py')
os.system('sudo ln -s '+cwd+'/displaydata.py /usr/bin/displaydata.py')
os.system('sudo ln -s '+cwd+'/config.yaml /usr/bin/config.yaml')
os.system('sudo ln -s '+cwd+'/buffer.txt /usr/bin/buffer.txt')
print 'SYMLINKS CREATED'
print 'ADDING AUTOSTARTS...'
os.system("printf '%s\n' '#!/bin/bash' 'nohup influxd &' 'nohup server.py &' 'exit 0' | sudo tee /etc/rc.local")
print 'AUTOSTARTS ADDED'
print 'REBOOT AND GOOD TO GO!'