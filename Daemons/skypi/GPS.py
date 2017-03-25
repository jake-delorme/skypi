import threading
import logging
import Queue
import sys
import os
import time
from gps import *


class GPS(object):

	def __init__(self,piManager,serialPort,baud):
		# create the object yo
		logging.debug("Create the GPS object")
		self.name = "GPS"
		self.serialPort = serialPort
		self.baudrate = baud
		self.piManager = piManager
		# Create the local queue
		self.Queue = Queue.PriorityQueue()
		# Create and start the threads
		self.listenerThread = threading.Thread(target=self.__listener, name=self.name+"-listener")
		self.listenerThread.daemon = True
		self.listenerThread.start()
		self.consumerThread = threading.Thread(target=self.__queueConsumer, name=self.name+"-consumer")
		self.consumerThread.daemon = True
		self.consumerThread.start()
		# GPS values
		self.gpsd = gps(mode=WATCH_ENABLE)
		self.lattitude = None
		self.longtitude = None
		self.height = None
		# Register for messages
		self.piManager.register(self,"SystemTest")
		self.piManager.register(self,"GetGPS")
		

	def __listener(self):
		name = threading.current_thread().getName()
		logging.debug("Running the "+name+" thread")
		
		while True:
			os.system('clear')

			print
			print ' GPS reading'
			print '----------------------------------------'
			print 'latitude    ' , self.gpsd.fix.latitude
			print 'longitude   ' , self.gpsd.fix.longitude
			print 'time utc    ' , self.gpsd.utc,' + ', self.gpsd.fix.time
			print 'altitude (m)' , self.gpsd.fix.altitude
			print 'eps         ' , self.gpsd.fix.eps
			print 'epx         ' , self.gpsd.fix.epx
			print 'epv         ' , self.gpsd.fix.epv
			print 'ept         ' , self.gpsd.fix.ept
			print 'speed (m/s) ' , self.gpsd.fix.speed
			print 'climb       ' , self.gpsd.fix.climb
			print 'track       ' , self.gpsd.fix.track
			print 'mode        ' , self.gpsd.fix.mode
			print
			print 'sats        ' , self.gpsd.satellites
			time.sleep(10)



	def addToQueue(self,event,priority=99):
		self.Queue.put( (priority,event) ) 
		
	def __queueConsumer(self):
		name = threading.current_thread().getName()
		logging.debug("Running the "+name+" thread")
		# process queue objects as the come in run the thread forever
		while 1:
			item = self.Queue.get(True)
			task = item[1].getTask()
			logging.debug("Process Queue task "+task )