import threading
import logging
import Queue
import sys
import os
import time
from gps import *
import pprint
import calendar
import re
pp = pprint.PrettyPrinter(indent=4)

class GPS(object):

	def __init__(self,piManager):
		# create the object yo
		logging.debug("Create the GPS object")
		self.name = "GPS"
		self.piManager = piManager
		# Create the local queue
		self.Queue = Queue.PriorityQueue()
		
		# GPS values
		self.gpsd = gps(mode=WATCH_ENABLE)
		self.lattitude = None
		self.longtitude = None
		self.height = None
		
		# Register for messages
		self.piManager.register(self,"SystemTest")
		self.piManager.register(self,"GetGPS")

		# Create and start the threads
		self.listenerThread = threading.Thread(target=self.__listener, name=self.name+"-listener")
		self.listenerThread.daemon = True
		self.listenerThread.start()
		self.consumerThread = threading.Thread(target=self.__queueConsumer, name=self.name+"-consumer")
		self.consumerThread.daemon = True
		self.consumerThread.start()
		
		

	def __listener(self):
		name = threading.current_thread().getName()
		logging.debug("Running the "+name+" thread")
		
		while True:
			data = self.gpsd.next()
			if re.match('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.000Z', self.gpsd.utc):
				parsedTime =  time.strptime(self.gpsd.utc, "%Y-%m-%dT%H:%M:%S.000Z")
				parsedEpoch =  calendar.timegm(parsedTime)
				logging.debug('Epoch time as parsed %s', parsedEpoch)
			logging.debug( 'latitude    %s' , self.gpsd.fix.latitude  )
			logging.debug( 'longitude   %s' , self.gpsd.fix.longitude )
			logging.debug( 'time utc    %s + %s' , self.gpsd.utc , self.gpsd.fix.time )
			logging.debug( 'altitude (f) %s' , self.gpsd.fix.altitude*3.28084 )
#			logging.debug( 'eps         ' , self.gpsd.fix.eps)
#			logging.debug( 'epx         ' , self.gpsd.fix.epx)
#			logging.debug( 'epv         ' , self.gpsd.fix.epv)
#			logging.debug( 'ept         ' , self.gpsd.fix.ept)
#			logging.debug( 'speed (m/s) ' , self.gpsd.fix.speed)
#			logging.debug( 'climb       ' , self.gpsd.fix.climb)
#			logging.debug( 'track       ' , self.gpsd.fix.track)
#			logging.debug( 'mode        ' , self.gpsd.fix.mode)
#			logging.debug('')
#			logging.debug( 'sats        ' , self.gpsd.satellites)
			



	def addToQueue(self,event,priority=99):
		self.Queue.put( (priority,event) ) 
		
	def __queueConsumer(self):
		name = threading.current_thread().getName()
		logging.debug("Running the %s thread" , name)
		# process queue objects as the come in run the thread forever
		while 1:
			item = self.Queue.get(True)
			task = item[1].getTask()
			logging.debug("Process Queue task %s" , task )