#!/usr/bin/python
import datetime
from flask import Flask  
from flask import render_template
from flask import request
from influxdb import InfluxDBClient
import os

cwd = os.getcwd()
app = Flask(__name__, template_folder = cwd + '/templates', static_folder = cwd + '/static')
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('test')

@app.route("/")
def hello():  
    message = "Hello, World"
    return render_template('index.html', message=message)

@app.route('/start', methods = ['POST'])
def start():
    os.system('clear')
    print request.values
    filename = str(request.values.get("Filename"))
    serial = str(request.values.get("Serial"))
    model = str(request.values.get("Model"))
    purpose = str(request.values.get("Purpose"))
    print filename, serial, model, purpose
    os.system('python start.py {0} {1} {2} {3}'.format(serial, model, purpose, filename))
    return 'Success'
        
@app.route('/database', methods = ['POST'])
def command():
    client.switch_database('test')
    query = str(request.values.get('query'))
    measurement = str(request.values.get('measurement'))
    batch = str(request.values.get('batchsize'))
    if query == 'DROP':
        client.drop_measurement(measurement)
        return 'Success'
    elif query == 'SHOW':
        results = list(client.query("SHOW MEASUREMENTS").get_points())
        return str([str(i['name']) for i in results])
    elif query == 'SELECT':
        os.system('clear')
        print 'should be select'
        print query + ' "STACK_I","STACK_V","OUTPUT_POWER","STACK_TEMP"' + ' FROM ' + measurement + ' GROUP BY * ORDER BY DESC LIMIT ' + batch
        print client._database
        start = datetime.datetime.now()
        results = client.query(query + ' "STACK_I","STACK_V","OUTPUT_POWER","STACK_TEMP"' + ' FROM ' + measurement + ' GROUP BY * ORDER BY DESC LIMIT ' + batch, epoch='ms')
        print 'TOOK ',(datetime.datetime.now()-start).seconds,' TO GET DATA'
        #print [i[j] for j in i.keys() for i in list(results.get_points(measurement=measurement)) if str(j) in ['time', 'STACK_V', 'STACK_I', 'STACK_TEMP', 'OUTPUT_POWER']]
        results = list(results.get_points(measurement=measurement))

        print str(results)
        print 'TOOK ',(datetime.datetime.now()-start).seconds,' TO LIST DATA'
        results = [{str(k):str(v) for k,v in i} for i in results]
        #results = [{str(k):float(v.replace('A', '').replace('V', '').replace('+', '').replace('C', '').replace('Z', '')) for k,v in i.items() if k in ['time', 'STACK_V', 'STACK_I', 'STACK_TEMP', 'OUTPUT_POWER']} for i in results]
        #results = [{str(k):float(''.join([l for l in str(v) if l in [str(m) for m in range(10)] + ['.']])) for k,v in i.items() if k in ['time', 'STACK_V', 'STACK_I', 'STACK_TEMP', 'OUTPUT_POWER']} for i in results]
        print 'TOOK ',(datetime.datetime.now()-start).seconds,' TO FILTER AND CHECK DATA, NOW RETURNING...'
        print str(results)
        return str(results)
    else:
        return 'Dab'
# run the application
if __name__ == "__main__":  
    os.chdir('/home/pi/boc-stuff/webserver')
    print os.getcwd()
    app.run(debug=True, port=80)
    
