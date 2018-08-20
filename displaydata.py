import time
import maxprint

dataVariables = ['STACK_V', 
             'STACK_I',
             'OUTPUT_2_V',
             'OUTPUT_1_I',
             'OUTPUT_POWER',
             'TIME_ELAPSED',
             'TARGET_TEMP',
             'STACK_TEMP',
             'FAN_DUTY',
             'AMB_TEMP',
             'INTERNAL_BATT_V', 
             'OUTPUT_1_V',
             'START_STOP_CYCLES',
             'TARGET_V', 
             'FIRMWARE',
             'MAX_P_W',
             'POWER_1_W',
             'POWER_2_W',
             'RUNTIME_SEC',
             'DATE',
             'TIME']

while True:
    with open('buffer.txt', 'r') as f:
        bufferData = eval(f.read())
    data, serial = eval(bufferData[0]), bufferData[1]
    if data != '':
        print_ = maxprint.Print(data, dataVariables)
        print print_._print()
    time.sleep(1)