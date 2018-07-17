import console
import time
a = console.Console()
variables = ['STACK_V', 
             'STACK_I',
             'STACK_TEMP',
             'AMB_TEMP',
             'INTERNAL_BATT_V', 
             'FAN_DUTY',
             'TARGET_TEMP',
             'OUTPUT_1_V',
             'START_STOP_CYCLES',
             'TARGET_V', 
             'OUTPUT_2_V',
             'FIRMWARE',
             'MAX_P_W',
             'POWER_1_W',
             'POWER_2_W',
             'RUNTIME_SEC',
             'DATE',
             'TIME']
while True:
    a.displayData(variables)
    time.sleep(1)