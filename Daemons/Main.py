#!/usr/bin/python
"""One Script to Rule them all. The heart of the SkyPi"""
import ConfigParser
import os
import sys
import logging
import time
import skypi
#import Queue
#import threading

# The logging config
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s (%(threadName)-10s) %(message)s')

def main():
	"""Create all the Objects and get going"""
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
	pimanager = skypi.Manager()

	# Battery object
	#skypi.Battery(pimanager)

	# GSM object
	#skypi.GSM(pimanager)

	# GPS Object
	skypi.GPS(pimanager)

	# Camera object
	#skypi.Camera(pimanager)

	while True:
		# A GPS message
		event = skypi.Event("GetGPS", "lat")
		pimanager.addToQueue(event)

		# An All message
		event = skypi.Event("SystemTest", "")
		pimanager.addToQueue(event)

		time.sleep(6000)


main()
