import threading
import logging
import Queue
import sys
import os


class GPS(object):

	def __init__(self):
		# create the object yo
		logging.debug("Create the GPS object")
		self.name = "GPS"
		# Create the local queue
		self.Queue = Queue.PriorityQueue()
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

	def addToQueue(self,task,args,priority=99):
		self.Queue.put( (priority,task,args) ) 
		
	def __queueConsumer(self):
		name = threading.current_thread().getName()
		logging.debug("Running the "+name+" thread")
		# process queue objects as the come in run the thread forever
		while 1:
			item = self.Queue.get(True)
			logging.debug("Process Queue Item")