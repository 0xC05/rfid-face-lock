import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import pickle
import RPi.GPIO as GPIO
from time import sleep
import os
import re
import serial
import time 
relay_pin = [26]
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, 0)

with open('labels', 'rb') as f:
	dict = pickle.load(f)
	f.close()

camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 30
ledPin = 11
blinkDelay = .5
ledOn = False

userspath = os.getcwd() + '\\images\\'
userspath = userspath.replace('\\','/')
rfidlist = os.listdir(userspath)
print rfidlist


ser = serial.Serial('/dev/ttyACM0', 9600)


try:
    while True:
        read_serial = ser.readline()
	read_serial = read_serial.rstrip()
	count =0
	print read_serial

	if read_serial in rfidlist:

		rawCapture = PiRGBArray(camera, size=(1280, 720))

		faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
		recognizer = cv2.face.createLBPHFaceRecognizer()
		recognizer.load("trainer.yml")

		font = cv2.FONT_HERSHEY_SIMPLEX
		count =0
		start =time.time()
		for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			frame = frame.array
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
			for (x, y, w, h) in faces:
				roiGray = gray[y:y+h, x:x+w]

				id_, conf = recognizer.predict(roiGray)

				for name, value in dict.items():
					if value == id_:
						print(name)
				print(time.time())
				if conf <= 60:
					count = count +1
				
				if count > 5 or time.time() - start > 60:
					break

				else:
					GPIO.output(relay_pin, 0)
			print(start - time.time())
			

			if count > 5 or (time.time() - start) > 60:
				break

			rawCapture.truncate(0)

		if count > 5:
			print("ja beta ja jele zindagi")
			GPIO.output(relay_pin, 1)
		else:
			print("Bada a ya bakchod")
		cv2.destroyAllWindows()

except Exception, err:
    GPIO.cleanup()
    print Exception, err
