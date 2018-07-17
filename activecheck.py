#!/usr/bin/python2.7
import psutil
import os

for process in psutil.process_iter():
    if process.cmdline() == ['python', 'console.py']:
        os.system('kill -s 2 ' + process.pid)
       #if raw_input('Found an existing process, would you like to exit? (Y/N) ').lower() == 'y':
           