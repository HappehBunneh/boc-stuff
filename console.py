import yaml
import os
import sys
import serial
import gzip
import sendemail
import maxprint
import updateData
from datetime import datetime
import time

class Console():
    def __init__(self):
        self.startTime = datetime.now()
        self.currentTime = datetime.now()
        with open('config.yaml', 'r') as f:
            config = yaml.load(f)
            self.dataVariables =  config['dataVariables']
            self.additionalVariables = config['additionalVariables']
            self.port = config['port']
            self.bufferLocation = config['buffer']
            self.dirLocation = config['test_directory']
            self.recipients = config['recipients']
            self.email = config['emailusr']
            self.pwd = config['emailpwd']
        self.data = {}
        self.serial = serial.Serial(port=self.port)    
        self.time_elapsed = 0;

    def setup(self):
        self.maxprint = maxprint.Print(self.data, self.dataVariables + self.additionalVariables)

    def getRawData(self):
        raw_data = self.serial.readline().replace('\r\n', '').replace('\r', ' ')[:-1]
        if raw_data == '':
            return [False]
        else:
            raw_data = [i for i in raw_data.split(' ') if i != '']
            self.raw_data =  raw_data
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
                    data['TIME_ELAPSED'] = self.time_elapsed
                    data['OUTPUT_POWER'] = str(float(data['OUTPUT_1_I'].replace('A', '')) * float(data['OUTPUT_2_V'].replace('V', '')))
                    return [' '.join(comments), data]
                elif len(raw_data) < len(self.dataVariables):
                    comments = raw_data
                    return [' '.join(comments), False]
                else:
                    return [False]

    def storeData(self, data):
        toWriteToFile = ''
        toWriteToBuffer = ''
        if len(data) == 1:
            if data[0]:
                data = data[0]
                toWriteToFile = '\n' + ','.join([data[i] for i in (self.dataVariables + self.additionalVariables)])
                toWriteToBuffer = str(data)
                self.data = data
        else:
            if data[1]:
                comments = data[0]
                data = data[1]
                toWriteToFile = '\n' + ','.join([data[i] for i in (self.dataVariables + self.additionalVariables)]) + ',' + comments
                self.data = data
            else:
                comments = data[0]
                toWriteToFile = ',' + comments
        with open(self.bufferLocation, 'w') as buffer:
            buffer.write(str([toWriteToBuffer, self.raw_data]))
        if self.fileLocation:
            with open(self.fileLocation, 'a') as f:
                f.write(toWriteToFile)

    def displayData(self, dataVariables=None):
        if dataVariables == None:
            dataVariables = self.dataVariables
        self.maxprint.dataVariables = dataVariables + self.additionalVariables
        with open(self.bufferLocation, 'r') as buffer:
            try:
                data = eval(buffer.read())[0]
            except Exception:
                data = ''
        if type(data) == dict:
            self.maxprint.data = data
            os.system('clear')
            a = self.maxprint._print()
            sys.stdout.write(a)
            sys.stdout.flush()
        

    def addTime(self):
        with open(self.fileLocation, 'a') as f:
            f.write('\nTime elapsed,' + str(self.time_elapsed))

    def compress(self):
        data = open(self.fileLocation).read()
        output = gzip.open(self.fileLocation + '.gz', 'wb')
        output.write(data)
        output.close()

if __name__ == '__main__':
    a = Console()
    while True:
        modelType = raw_input('\nSpecify model type : ')
        if '150' in modelType or '200' in modelType:
            a.dataVariables = a.dataVariables['150/200']
            a.setup()
            break
        else:
            print '\nPlease specifiy a valid modelType'
            print 'Models I have include... ' + ','.join(a.dataVariables)

    serialNumber = raw_input('\nSpecify serial number : ')
    testReason = raw_input('\nPurpose of test : ')
    while True:
        a.fileLocation = a.dirLocation + '/' + raw_input('\nSpecify filename : ') + '.csv'
        if os.path.exists(a.fileLocation):
            if raw_input('\nAlready exists, would you like to overwrite this... (Y/N) ? ').lower() == 'y':
                os.remove(a.fileLocation)
                break
            else:
                sys.stdout.write('\n')
                sys.stdout.flush()
        else:
            break
    with open(a.fileLocation, 'w') as f:
        f.write('Model_Type' + ',' + modelType + '\n')
        f.write('Serial_Number' + ',' + serialNumber + '\n')
        f.write('Test_Reason' + ',' + testReason + '\n')
        f.write('\n')
        f.write(','.join(a.dataVariables + a.additionalVariables) + '\n')
    b = sendemail.Mail(a.email, a.pwd, a.recipients, a.fileLocation + '.gz')
    c = updateData.Database()
    while True:
        try:
            a.currentTime = datetime.now()
            days, seconds = (a.currentTime - a.startTime).days, (a.currentTime - a.startTime).seconds
            a.time_elapsed = str((days * 24) + round((float(seconds) / 3600), 3))
            data = a.getRawData()
            print data
            if data[0]:
                a.storeData(data)
                if 'STACK_I' in a.data.keys():
                    try:
                        current = float(a.data['STACK_I'].replace('A', ''))
                        voltage = float(a.data['STACK_V'].replace('V', ''))
                        temp = float(a.data['STACK_TEMP'].replace('C', ''))
                        power = float(a.data['OUTPUT_POWER'])
                        c.update(current, power, temp, voltage)
                    except Exception:
                        pass
                a.displayData()
        except (KeyboardInterrupt, SystemExit):
            a.addTime()
            a.compress()
            b.sendMail()
            exit()
       