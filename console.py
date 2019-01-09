#!/usr/bin/python
import yaml
import os
import sys
import maxprint
import serial
from datetime import datetime
import time
from influxdb import InfluxDBClient
import pandas as pd

class Console():
    def __init__(self, serialNumber, model, testReason, fileName, port, baudrate):
        with open('/usr/bin/hym_config.yaml', 'r') as f:
            config = yaml.load(f)
        # Configuration for serial...
        self.baudrate = baudrate
        self.port = port
        # Configuration for log file/database...
        self.model = model
        self.serialNumber = serialNumber
        self.fileName = fileName
        self.testReason = testReason
        # Configuration for python process...
        self.bufferLocation = config['buffer']
        self.dataVariables = config['dataVariables'][model]
        self.additionalVariables = config['additionalVariables']
        self.data = {}
        self.comments = []
        self.client = InfluxDBClient(host='localhost', port=8086)
        self.client.switch_database('test')
        self.maxprint = maxprint.Print(self.data, self.dataVariables + self.additionalVariables)

    def readline(self):
        line = bytearray()
        while True:
            c = self.serial.read()
            if c:
                line += c
                if line[-2:] in ['\r\r', '\r\n']:
                    break
            else:
                break
        return bytes(line)

    def getData(self):
        self.currentTime = datetime.now()
        days, seconds = (self.currentTime - self.startTime).days, (self.currentTime - self.startTime).seconds
        self.time_elapsed = str((days * 24) + round((float(seconds) / 3600), 3))
        #if self.model == '150/200':
        #    raw_data = self.readline(b'\r\n\r\n').replace('\r\n', '').replace('\r', ' ')[:-1]
        #else:
        #    raw_data = self.readline().replace('\r\n', '').replace('\r', ' ')[:-1]
        raw_data = self.readline().replace('\r\n', '').replace('\r\r', '').replace('\r', ' ')[:-1]
        if raw_data == '':
            return [False]
        else:
            raw_data = [i for i in raw_data.split(' ') if i != '']
            self.raw_data = raw_data
            if len(raw_data) == len(self.dataVariables):
                data  = dict(zip(self.dataVariables, raw_data))
                data['TIME_ELAPSED'] = self.time_elapsed
                data['OUTPUT_POWER'] = str(float(data['OUTPUT_1_I'].replace('A', '')) * float(data['OUTPUT_2_V'].replace('V', '')))
                return [data]
            else:
                if len(raw_data) > len(self.dataVariables):
                    comments = raw_data[:-len(self.dataVariables)]
                    data = raw_data[len(raw_data)-len(self.dataVariables):]
                    data = dict(zip(self.dataVariables, data))
                    print comments, data
                    data['TIME_ELAPSED'] = self.time_elapsed
                    data['OUTPUT_POWER'] = str(float(data['OUTPUT_1_I'].replace('A', '')) * float(data['OUTPUT_2_V'].replace('V', '')))
                    return [' '.join(comments), data]
                elif len(raw_data) < len(self.dataVariables):
                    comments = raw_data
                    return [' '.join(comments), False]
                else:
                    return [False]

    def saveData(self, data):
        if len(data) == 1:
            if data[0]:
                self.data = data[0]
                self.client.write_points([{'fields': self.data, 'measurement': self.fileName.replace('/', '_')}])
                self.comments = []
        else:
            if data[1]:
                self.comments = data[0]
                self.data = data[1]
                self.client.write_points([{'fields': self.data, 'measurement': self.fileName.replace('/', '_')}])
                self.comments = []
            else:
                self.comments += data[0]
        with open(self.bufferLocation, 'w') as buffer:
            buffer.write(str([self.data, self.comments]))
        
    def displayData(self, dataVariables=None):
        if dataVariables == None:
            dataVariables = self.dataVariables
        self.maxprint.dataVariables = dataVariables + self.additionalVariables
        with open(self.bufferLocation, 'r') as buffer:
            try:
                data = eval(buffer.read())[0]
            except Exception:
                data = ''
        print data, type(data)
        if type(data) == dict:
            self.maxprint.data = data
            os.system('clear')
            a = self.maxprint._print()
            sys.stdout.write(a)
            sys.stdout.flush()

    def close(self):
        #read dataframe and create .csv file.......
        #first = self.client.query("select BOTTOM(STACK_V, 1) from " + self.fileName.replace('/', '_'))
        #last = self.client.query('select TOP(STACK_V, 1) from ' + self.fileName.replace('/', '_'))
        #make these datetime objects...
        #first = datetime.strptime(first, '%Y-%m-%dT%H:%M:%SZ')
        #last = datetime.strptime(last, '%Y-%m-%dT%H:%M:%SZ')
        os.system('clear')
        os.environ['running'] = 'False'
        print 'Ending process and generating logfile...'
        q = 'select * from ' + self.fileName.replace('/', '_')
        df = pd.DataFrame(self.client.query(q, chunked=True, chunk_size=10000).get_points())
        with open(self.fileName + '.csv', 'w+') as logfile:
            logfile.write('Model_Type' + ',' + self.model + '\n')
            logfile.write('Serial_Number' + ',' + self.serialNumber + '\n')
            logfile.write('Test_Reason' + ',' + self.testReason + '\n')
            logfile.write('\n')
            #logfile.write(','.join(self.dataVariables + self.additionalVariables) + '\n')
            df.to_csv(logfile, header=True)
        print 'Finished writing'
        exit()
    
    def startReadingPort(self):
        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate)
        print 'serial started...'

    def run(self):
        print 'writing os variables'
        os.environ['running'] = 'True'
        os.environ['filename'] = self.fileName
        print 'running...'
        self.startReadingPort()
        self.currentTime = datetime.now()
        self.startTime = self.currentTime
        raw_data = self.readline().replace('\r\n', '').replace('\r\r', '').replace('\r', ' ')[:-1]
        raw_data = [i for i in raw_data.split(' ') if i not in ['', '\x00']]
        print raw_data, len(raw_data)
        while True:
            try:
                data = self.getData()
                if data[0]:
                    #os.system('clear')
                    self.saveData(data)
                    self.displayData()
            except (KeyboardInterrupt, SystemExit):
                self.close()         

if __name__ == '__main__':
    with open('/usr/bin/hym_config.yaml', 'r') as f:
            config = yaml.load(f)
    while True:
        model = raw_input('\nSpecify model type : ')
        if '150' in model or '200' in model:
            model = '150/200'
            break
        elif '60' in model:
            model = 'OLD'
            break
        elif 'old' in model.lower():
            model = 'VOLD'
            break
    serialNumber = raw_input('\nSpecify serial number : ')
    testReason = raw_input('\nPurpose of test : ')
    while True:
        fileName = config['test_directory']+'/'+model+'_'+serialNumber+'_'+testReason.replace(' ', '_')+'_'+time.strftime('%d%m/%Y')
        #fileName = config['test_directory'] + '/' + raw_input('\nSpecify filename : ')
        if os.path.exists(fileName):
            if raw_input('\nAlready exists, would you like to overwrite this... (Y/N) ? ').lower() == 'y':
                os.remove(fileName)
                break
            else:
                sys.stdout.write('\n')
                sys.stdout.flush()
        else:
            break
    console = Console(serialNumber, model, testReason, fileName, config['port'], config['baudrate'])
    console.run()

