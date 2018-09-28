import sys
from console_2 import Console
import yaml
import os

with open('config.yaml') as config:
    config = yaml.load(config)

if len(sys.argv) != 5:
    while True:
        model = raw_input('\nSpecify model type : ')
        if '150' in model or '200' in model:
            model = '150/200'
            break
        elif '60' in model:
            model = '60'
            break
        elif 'old' in model.lower():
            model = 'OLD'
            break
    serialNumber = raw_input('\nSpecify serial number : ')
    testReason = raw_input('\nPurpose of test : ')
    while True:
        fileName = config['test_directory'] + '/' + raw_input('\nSpecify filename : ')
        if os.path.exists(fileName):
            if raw_input('\nAlready exists, would you like to overwrite this... (Y/N) ? ').lower() == 'y':
                os.remove(fileName)
                break
            else:
                sys.stdout.write('\n')
                sys.stdout.flush()
        else:
            break
    port = config['port']
    baudrate = config['baudrate']
    Console(serialNumber, model, testReason, fileName, port, baudrate).run()
else:
    filename = sys.argv[1]
    while True:
        fileName = config['test_directory'] + '/' + filename
        if os.path.exists(fileName):
            if raw_input('\nAlready exists, would you like to overwrite this... (Y/N) ? ').lower() == 'y':
                os.remove(fileName)
                break
            else:
                sys.stdout.write('\n')
                sys.stdout.flush()
        else:
            break
    model = sys.argv[2]
    purpose = sys.argv[3]
    serial = sys.argv[4]
    port = config['port']
    baudrate = config['baudrate']
    Console(serial, model, purpose, filename, port, baudrate).run()