from flask import Flask  
from flask import render_template
from flask import request
from influxdb import InfluxDBClient
import os

app = Flask(__name__)
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
    query = str(request.values.get('query'))
    measurement = str(request.values.get('measurement'))
    batch = str(request.values.get('batchsize'))
    if query == 'DROP':
        client.drop_measurement(measurement)
        return 'Success'
    elif query == 'SHOW':
        results = client.get_list_measurements()
        return str([str(i['name']) for i in results])
    elif query == 'SELECT':
        os.system('clear')
        print 'should be select'
        print query + ' ' + batch + ' FROM ' + measurement
        results = client.query(query + ' ' + batch + ' FROM ' + measurement, epoch='s')
        #print [i[j] for j in i.keys() for i in list(results.get_points(measurement=measurement)) if str(j) in ['time', 'STACK_V', 'STACK_I', 'STACK_TEMP', 'OUTPUT_POWER']]
        results = list(results.get_points(measurement=measurement))
        #results = [{str(k):float(v.replace('A', '').replace('V', '').replace('+', '').replace('C', '').replace('Z', '')) for k,v in i.items() if k in ['time', 'STACK_V', 'STACK_I', 'STACK_TEMP', 'OUTPUT_POWER']} for i in results]
        results = [{str(k):float(str(v).replace('A', '').replace('V', '').replace('+', '').replace('C', '')) for k,v in i.items() if k in ['time', 'STACK_V', 'STACK_I', 'STACK_TEMP', 'OUTPUT_POWER']} for i in results]
        return str(results)
    else:
        return 'Dab'
# run the application
if __name__ == "__main__":  
    app.run(debug=True, port=80)
    