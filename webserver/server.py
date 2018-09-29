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
    global client
    query = str(request.values.get("query"))
    results = client.query(query)
    return results
# run the application
if __name__ == "__main__":  
    global client
    app.run(debug=True, port=80)
    