import threading
import logging
import Queue
import sys
import os
import time
import serial
import pynmea2


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
		self.lattitude = None
		self.longtitude = None
		self.height = None
		# Register for messages
		self.piManager.register(self,"SystemTest")
		self.piManager.register(self,"GetGPS")
		

	def __listener(self):
		name = threading.current_thread().getName()
		logging.debug("Running the "+name+" thread")
		reader = pynmea2.NMEAStreamReader()

		while True:
			com = None
			try:
				com = serial.Serial(port=self.serialPort,baudrate=self.baudrate, timeout=5.0)
			except serial.SerialException:
				logging.error('Could not connect to %s' % self.serialPort)
				time.sleep(5.0)
				continue

			data = com.read(16)
			for msg in reader.next(data):
				logging.info(msg)


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