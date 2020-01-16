import RPi.GPIO as GPIO
import serial
import re
import os

ledPin = 11
blinkDelay = .5
ledOn = False

userspath = os.getcwd() + '\\images\\'
userspath = userspath.replace('\\','/')
rfidlist = os.listdir(userspath)
print rfidlist

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledPin, GPIO.OUT)

ser = serial.Serial('/dev/ttyACM0', 9600)

try:
    while True:
        read_serial = ser.readline()
	read_serial = read_serial.rstrip()

	print read_serial

	if read_serial in rfidlist:
		print 'PASS'
	else:
		print 'FAIL'

except Exception, err:
    GPIO.cleanup()
    print Exception, err
