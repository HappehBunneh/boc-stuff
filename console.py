import yaml
import os
import sys
import serial

class Console():
    def __init__(self):
        with open('config.yaml', 'r') as f:
            config = yaml.load(f)
            self.dataVariables =  config['dataVariables']
            self.port = config['port']
            self.bufferLocation = config['buffer']
            self.fileLocation = config['fileLocation']
        self.serial = serial.Serial(port=self.port)    

    def getRawData(self):
        raw_data = self.serial.readline().replace('\r\n', '').replace('\r', ' ')[:-1]
        print raw_data
        if raw_data == '':
            return [False]
        else:
            raw_data = raw_data.split(' ')
            if len(raw_data) == len(self.dataVariables):
                return [dict(zip(self.dataVariables, raw_data))]
            else:
                if len(raw_data) > len(self.dataVariables):
                    comments = raw_data[:-len(self.dataVariables)]
                    data = raw_data[len(self.dataVariables):]
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

    def displayData(self):
        with open(self.bufferLocation, 'r') as buffer:
            try:
                data = eval(buffer.read())
            except Exception:
                data  = ''
        if type(data) == dict:
            os.system('clear')
            a = ''
            b = [i for i in self.dataVariables if 'IGNORE' not in i]
            for i in range(len(b)):
                if i % 4 == 0 and i != 0:
                    a += b[i] + '\t\t' + data[b[i]] + '\t\t'
                else:
                    a += '\n' + b[i] + '\t\t' + data[b[i]] + '\t\t'
            sys.stdout.write(a)
            sys.stdout.flush()

if __name__ == '__main__':
    a = Console()
    modelType = raw_input('\nSpecify model type : ')
    serialNumber = raw_input('\nSpecify serial number : ')
    testReason = raw_input('\nPurpose of test : ')
    while True:
        a.fileLocation = raw_input('\nSpecify filename : ') + '.csv'
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
    while True:
        data = a.getRawData()
        print data
        if data[0] and len(data) == 0:
            a.storeData(data)
        a.displayData()