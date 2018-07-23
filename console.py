import yaml
import os
import sys
import serial
import gzip
import sendemail
import maxprint
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
        self.maxprint = maxprint.Print(self.data, self.dataVariables + self.additionalVariables)
        self.serial = serial.Serial(port=self.port)    
        self.time_elapsed = 0;

    def getRawData(self):
        raw_data = self.serial.readline().replace('\r\n', '').replace('\r', ' ')[:-1]
        if raw_data == '':
            return [False]
        else:
            raw_data = [i for i in raw_data.split(' ') if i != '']
            if len(raw_data) == len(self.dataVariables):
                return [dict(zip(self.dataVariables, raw_data))]
            else:
                if len(raw_data) > len(self.dataVariables):
                    comments = raw_data[:-len(self.dataVariables)]
                    data = raw_data[len(raw_data)-len(self.dataVariables):]
                    return [' '.join(comments), dict(zip(self.dataVariables, data))]
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
                toWriteToFile = '\n' + ','.join([data[i] for i in self.dataVariables])
                data['TIME_ELAPSED'] = self.time_elapsed
                data['POWER'] = str(float(data['STACK_V'].replace('V', '')) * float(data['STACK_I'].replace('A', '')))
                toWriteToBuffer = str(data)
        else:
            if data[1]:
                comments = data[0]
                data = data[1]
                toWriteToFile = '\n' + ','.join([data[i] for i in self.dataVariables]) + ',' + comments
            else:
                comments = data[0]
                toWriteToFile = ',' + comments
        if toWriteToBuffer != '':
            with open(self.bufferLocation, 'w') as buffer:
                buffer.write(toWriteToBuffer)
        if self.fileLocation:
            with open(self.fileLocation, 'a') as f:
                f.write(toWriteToFile)

    def displayData(self, dataVariables=None):
        if dataVariables == None:
            dataVariables = self.dataVariables
        self.maxprint.dataVariables = dataVariables + self.additionalVariables
        with open(self.bufferLocation, 'r') as buffer:
            try:
                data = eval(buffer.read())
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
    modelType = raw_input('\nSpecify model type : ')
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
        f.write(','.join(a.dataVariables) + '\n')
    b = sendemail.Mail(a.email, a.pwd, a.recipients, a.fileLocation + '.gz')
    
    while True:
        try:
            a.currentTime = datetime.now()
            a.time_elapsed = relativedelta(a.currentTime, a.startTime)
            data = a.getRawData()
            if data[0]:
                a.storeData(data)
            a.displayData()
           
        except (KeyboardInterrupt, SystemExit):
            a.addTime()
            a.compress()
            b.sendMail()
            exit()
       