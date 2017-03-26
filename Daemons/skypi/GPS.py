"""Manages retrieving data from our GPSD daemon"""
import threading
import logging
import Queue
import time
import calendar
import re
from gps import *
from skypi.Manager import Event


class GPS(object):
	"""Runs a thread for retrieving GPS status and a queue for giving location"""
	def __init__(self, pimanager):
		# create the object yo
		logging.debug("Create the GPS object")
		self.name = "GPS"
		self.pimanager = pimanager
		# Create the local queue
		self.queue = Queue.PriorityQueue()

		# GPS object
		self.gpsd = gps(mode=WATCH_ENABLE)
		self.gpslocation = Gpslocation()

		# Register for messages
		self.pimanager.register(self, "SystemTest")
		self.pimanager.register(self, "GetGPS")

		# Create and start the threads
		self.listenerthread = threading.Thread(target=self.__listener, name=self.name+"-listener")
		self.listenerthread.daemon = True
		self.listenerthread.start()
		self.consumerthread = threading.Thread(target=self.__queueconsumer, name=self.name+"-consumer")
		self.consumerthread.daemon = True
		self.consumerthread.start()

	def __listener(self):
		"""Continuously read the GPS data and update the gpslocation object"""
		name = threading.current_thread().getName()
		logging.debug("Running the "+name+" thread")

		while True:
			self.gpsd.next()
			# match only if we got a valid date (partial fix)
			if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.000Z', self.gpsd.utc):
				# convert utc to epoch
				parsedtime = time.strptime(self.gpsd.utc, "%Y-%m-%dT%H:%M:%S.000Z")
				parsedepoch = calendar.timegm(parsedtime)
				# 2 = 2D_FIX 3 = 3D_FIX
				if self.gpsd.fix.mode > 1:
					self.gpslocation.lattitude = self.gpsd.fix.latitude
					self.gpslocation.longtitude = self.gpsd.fix.longitude
					self.gpslocation.lastfix = parsedepoch
					if self.gpsd.fix.mode == 3:
						self.gpslocation.altitude = self.gpsd.fix.altitude*3.28084
						self.gpslocation.lastaltitudefix = parsedepoch

#			logging.debug('GPS fix mode %s', self.gpsd.fix.mode)
#			logging.debug( 'latitude    %s' , self.gpsd.fix.latitude  )
#			logging.debug( 'longitude   %s' , self.gpsd.fix.longitude )
#			logging.debug( 'time utc    %s + %s' , self.gpsd.utc , self.gpsd.fix.time )
#			logging.debug( 'altitude (f) %s' , self.gpsd.fix.altitude*3.28084 )
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

	def addToQueue(self, event, priority=99):
		"""Adds an item to the GPS queue to be processed"""
		self.queue.put((priority, event))

	def __queueconsumer(self):
		name = threading.current_thread().getName()
		logging.debug("Running the %s thread", name)
		# process queue objects as the come in run the thread forever
		while 1:
			item = self.queue.get(True)
			task = item[1].getTask()
			logging.debug("Process Queue task %s", task)
			if task == "GetGPS" or task == "SystemTest":
				event = Event("GPSLocation", self.gpslocation)
				self.pimanager.addToQueue(event)
			else:
				logging.error('Recieved message %s but i dont use this message', task)
			self.queue.task_done()

class Gpslocation(object):
	"""Holds the current GPSStatus including location"""
	def __init__(self):
		self.lattitude = 'Nan'
		self.longtitude = 'Nan'
		self.altitude = 'Nan'
		self.lastfix = 0
		self.lastaltitudefix = 0
