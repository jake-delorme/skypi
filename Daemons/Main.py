#!/usr/bin/python
import ConfigParser
import os
import sys
import logging
import threading
import Queue
import time

# Import all the other classes
import GSM
import Battery
import GPS
import Camera
import Manager

# The logging config
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s (%(threadName)-10s) %(message)s')

def Main():
	config = ConfigParser.SafeConfigParser()
	try:
		config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + "/config.ini"))
	except IOError:
		print "Cannot find configuration file " + os.path.dirname(os.path.abspath(__file__)) + "/config.ini"
		sys.exit(1)

	for section in config.sections():
		for key in config.items(section):
			print section + " - " + key[0] + " - " + key[1]


	# Create the manager object
	piManager = Manager.Manager()

	# Battery object
	piBattery = Battery.Battery(piManager)
	piBattery.addToQueue("Check","%")

	# GSM object
	piGSM = GSM.GSM(piManager)
	piGSM.addToQueue("SendSMS","Im Alive!",priority=1)

	# GPS Object
	piGPS = GPS.GPS(piManager)
	piGPS.addToQueue("Update","Height",priority=2)

	# Camera object
	piCamera = Camera.Camera(piManager)
	piCamera.addToQueue("Selfie!","")

	time.sleep(1)


Main()



