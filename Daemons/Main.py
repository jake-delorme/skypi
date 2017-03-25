#!/usr/bin/python
import ConfigParser
import os
import sys
import logging
import threading
import Queue
import time
import skypi

# Import all the other classes
#import GSM
#import Battery
#import GPS
#import Camera
#import Manager

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
	piManager = skypi.Manager()

	# Battery object
	piBattery = skypi.Battery(piManager)

	# GSM object
	piGSM = skypi.GSM(piManager)
	
	# GPS Object
	piGPS = skypi.GPS(piManager,config.get("GPS","port"),config.get("GPS","baudrate"))

	# Camera object
	piCamera = skypi.Camera(piManager)


	while True:
		# A GPS message 
		event = skypi.Event("GetGPS","lat")
		piManager.addToQueue(event)

		# An All message
		event = skypi.Event("SystemTest","")
		piManager.addToQueue(event)

		time.sleep(5)


Main()



