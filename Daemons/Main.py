#!/usr/bin/python
"""One Script to Rule them all. The heart of the SkyPi"""
import ConfigParser
import os
import sys
import logging
import time
import skypi
import Queue
import threading

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

	# Create the manager object (router)
	pimanager = skypi.Manager()

	# Main Queue 
	mainqueue = Mainqueue(pimanager)
	mainqueue.start()

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
		event = skypi.Event("GetGPS", "")
		pimanager.addToQueue(event)

		# An All message
		#event = skypi.Event("SystemTest", "")
		#pimanager.addToQueue(event)

		time.sleep(5)


class Mainqueue(threading.Thread):

	def __init__(self, pimanager):
		super(Mainqueue,self).__init__()
		self.daemon = True
		self.pimanager = pimanager
		self.queue = Queue.PriorityQueue()
		self.name = 'MainQueue'
		self.registerformessages()

	def registerformessages(self):
		self.pimanager.register(self, "GPSLocation")

	def addToQueue(self, event, priority=99):
		"""Adds an item to the Main queue to be processed"""
		self.queue.put((priority, event))

	def run(self):
		name = threading.current_thread().getName()
		logging.debug('Running the %s thread', name)
		while True:
			item = self.queue.get(True)
			event = item[1]
			task = event.getTask()
			logging.debug("Process Queue task %s", task)

			# Here we will get the GPS location messages and ship them out over SMS
			if task == "GPSLocation":
				gpslocation = event.getargs()
				url = gpslocation.getgoogleurl()
				logging.info('Current location url %s', url)
			
			self.queue.task_done()




main()
