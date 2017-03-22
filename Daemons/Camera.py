import threading
import logging
import Queue
import time
import sys
import os


class Camera(object):

	def __init__(self,piManager):
		# create the object yo
		logging.debug("Create the Camera object")
		self.name = "Camera"
		self.lastImage = None
		self.piManager = piManager
		# Create the local queue
		self.Queue = Queue.PriorityQueue()
		# Create and start the threads
		self.captureThread = threading.Thread(target=self.__capture, name=self.name+"-capture")
		self.captureThread.daemon = True
		self.captureThread.start()
		self.consumerThread = threading.Thread(target=self.__queueConsumer, name=self.name+"-consumer")
		self.consumerThread.daemon = True
		self.consumerThread.start()

	def __capture(self):
		name = threading.current_thread().getName()
		logging.debug("Running the "+name+" thread")
		while True:
			# take picture
			# self.lastImage = blah
			time.sleep(30)

	def addToQueue(self,task,args,priority=99):
		self.Queue.put( (priority,task,args) ) 

	def getLastImage(self):
		return self.lastImage
		
	def __queueConsumer(self):
		name = threading.current_thread().getName()
		logging.debug("Running the "+name+" thread")
		# process queue objects as the come in run the thread forever
		while 1:
			item = self.Queue.get(True)
			logging.debug("Process Queue Item")