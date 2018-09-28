from influxdb import InfluxDBClient
import yaml
import maxprint

client = InfluxDBClient(host='localhost', port=8086)

with open('config.yaml', 'r') as config:
    config = yaml.load(config)

readVariables = config['readVariables']

while True:
    data = []
    for variable in readVariables:
        data.append(client.query('select BOTTOM(' + variable + ' ,1) from filename'))
    maxprint.Print(data, readVariables)
