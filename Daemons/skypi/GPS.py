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

			logging.debug()
			logging.debug( ' GPS reading')
			logging.debug( '----------------------------------------')
			logging.debug( 'latitude    ' , self.gpsd.fix.latitude)
			logging.debug( 'longitude   ' , self.gpsd.fix.longitude)
			logging.debug( 'time utc    ' , self.gpsd.utc,' + ', self.gpsd.fix.time)
			logging.debug( 'altitude (m)' , self.gpsd.fix.altitude)
			logging.debug( 'eps         ' , self.gpsd.fix.eps)
			logging.debug( 'epx         ' , self.gpsd.fix.epx)
			logging.debug( 'epv         ' , self.gpsd.fix.epv)
			logging.debug( 'ept         ' , self.gpsd.fix.ept)
			logging.debug( 'speed (m/s) ' , self.gpsd.fix.speed)
			logging.debug( 'climb       ' , self.gpsd.fix.climb)
			logging.debug( 'track       ' , self.gpsd.fix.track)
			logging.debug( 'mode        ' , self.gpsd.fix.mode)
			logging.debug()
			logging.debug( 'sats        ' , self.gpsd.satellites)
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