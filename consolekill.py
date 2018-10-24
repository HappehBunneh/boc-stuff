#!/usr/bin/python
import psutil
import os

for process in psutil.process_iter():
    if process.cmdline() == ['python', 'console.py']:
        if raw_input('Process running, would you like to kill it? (Y/N : ').lower() == 'y':
            os.system('kill -s 2 ' + str(process.pid))
       #if raw_input('Found an existing process, would you like to exit? (Y/N) ').lower() == 'y':
           