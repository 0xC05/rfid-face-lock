import RPi.GPIO as GPIO
import serial
import re
import os

ledPin = 11
blinkDelay = .5
ledOn = False

userspath = os.getcwd() + '\\images\\'
userspath = path.replace('\\','/')
rfidlist = os.listdir(userspath)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledPin, GPIO.OUT)

ser = serial.Serial('/dev/ttyACM0', 9600)

try:
    while True:
        GPIO.output(ledPin, False)
        GPIO.output(ledPin, True)

        read_serial = int(ser.readline())
        print read_serial

	if read_serial in rfidlist:
		print 'PASS'
	else:
		print 'FAIL'

except:
    GPIO.cleanup()
