#!/usr/bin/python
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)

GPIO.output(2, GPIO.LOW)
time.sleep(4)
GPIO.output(2, GPIO.HIGH)