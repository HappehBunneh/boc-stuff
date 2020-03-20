#!/usr/bin/python3
import os
import subprocess
import time
import sys
cwd = os.getcwd()

'''
This script installs influxDB and grafana, as well as creating necessary directories
with "appropriate" permissions
'''

os.system("sudo apt -y update")
os.system("sudo apt -y upgrade")
os.system("sudo apt -y install python3-pip")
#python3 requirements
subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "influxdb"])
os.system("wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -")
#make check
with open("/etc/os-release") as f:
    stuff = [i.strip("\n") for i in f.readlines()]
for i in stuff:
    if "VERSION_ID" in i:
        if i.split("=")[1] == "9":
            os.system('echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list')
        else:
            os.system('echo "deb https://repos.influxdata.com/debian buster stable" | sudo tee /etc/apt/sources.list.d/influxdb.list')
os.system("sudo apt-get update")
os.system("sudo apt -y install influxdb")
os.system("sudo systemctl unmask influxdb")
os.system("sudo systemctl enable influxdb")
os.system("sudo systemctl start influxdb")
while True:
    if os.popen("curl -sL -I localhost:8086").read() != "":
        break
print("Configuring database")
from influxdb import InfluxDBClient
client = InfluxDBClient(host="localhost", port=8086)
client.create_database("hymera")
os.system("wget https://dl.grafana.com/oss/release/grafana_6.6.1_armhf.deb")
os.system("sudo dpkg -i grafana_6.6.1_armhf.deb")
os.system("sudo systemctl enable grafana_server")
#edit grafana config to run on port :80
with open("/etc/grafana/grafana.ini") as f:
    data = f.readlines()
for i in range(len(data)):
    if data[i] == ";http_port = 3000\n":
        data[i] = "http_port = 80\n"
        break
with open("/etc/grafana/grafana.ini", "w") as f:
    for i in data:
        f.write(i)
os.system("sudo systemctl start grafana_sever")
os.system("sudo mkdir /var/lib/hymera")
os.system("sudo mkdir /var/log/hymera")
os.system("sudo chmod 666 /var/lib/hymera")
os.system("sudo chmod 666 /var/log/hymera")
os.system("touch /var/lib/hymera/status")
os.system("touch /var/lib/hymera/buffer")
os.system("touch /var/lib/hymera/PID")
#create grafana home dashboard *doing*
#move grafana dashboard template to /var/lib/hymera/template.json
import requests
os.system("curl -X POST http://admin:admin@localhost:80/api/user/using/1")
headers = {"Content-Type": "application/json"}
payload = {"name": "python", "role": "Admin"}
p =  requests.post("http://admin:admin@localhost:80/api/auth/keys", headers=headers, json=payload)
key = p.json()["key"]
with open("/var/lib/hymera/secret", "w") as f:
    f.write(key)
headers = {"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization" : "Bearer {0}".format(key)}
payload = {
    "name":"InfluxDB",
    "type":"influxdb",
    "url":"http://localhost:8086",
    "access":"proxy",
    "basicAuth":false,
    isDefault:true
}
p = requests.post("http://localhost:80/api/datasources", headers=headers, json=payload)
