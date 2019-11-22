import RPi.GPIO as GPIO
import serial
import re
import os

ledPin = 11
blinkDelay = .5
ledOn = False

rfidlist = []
rfidlistfile = open ("rfid/authcards.txt","r")
for line in rfidlistfile.readlines():
	for i in line.split():
		rfidlist.append(int(i))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledPin, GPIO.OUT)

ser = serial.Serial('/dev/ttyACM0',9600)

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
