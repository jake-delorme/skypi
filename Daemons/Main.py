#!/usr/bin/python
import ConfigParser
import os
import sys
import logging
import threading
import Queue

# Import all the other classes
import GSM
import Battery
import GPS
import Camera

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


	piBattery = Battery.Battery()
	piGSM = GSM.GSM()
	piGPS = GPS.GPS()
	piCamera = Camera.Camera()



Main()

