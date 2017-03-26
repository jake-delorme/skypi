import threading
import logging
import Queue
import sys
import os
import time
from gpiozero import MCP3008


class Battery(object):

	def __init__(self,piManager):
		# create the object yo
		logging.debug("Create the Battery object")
		self.name = "Battery"
		self.piManager = piManager
		# Create the local queue
		self.Queue = Queue.PriorityQueue()
		# The voltage mathing
		self.vref = 2.96
		self.r1 = 51000
		self.r2 = 6800
		self.correctionFactor = 1
		# Create and start the threads
		self.listenerThread = threading.Thread(target=self.__listener, name=self.name+"-listener")
		self.listenerThread.daemon = True
		self.listenerThread.start()
		self.consumerThread = threading.Thread(target=self.__queueConsumer, name=self.name+"-consumer")
		self.consumerThread.daemon = True
		self.consumerThread.start()
		# Register for messages
		self.piManager.register(self,"SystemTest")

	def __listener(self):
		name = threading.current_thread().getName()
		logging.debug('Running the %s thread', name)
		batV = MCP3008(0).value
		while True:
			voltage = self.__calculateBatteryVoltage()
			logging.debug('Battery voltage is %s', voltage )
			time.sleep(2)

	def __calculateBatteryVoltage(self):
		# The ratio the divider is dropping our voltage by
		divider = (self.r1 + self.r2) / float(self.r2) 
		logging.debug('Voltage divider modification %s', divider)
		# expand the value read from 0 - 1 back to its real value based on vref
		temp = MCP3008(0).value
		logging.debug('Read %s from MCP3008' , temp)
		value = MCP3008(0).value * self.vref

		# the output voltage is the divider * the value
		rawVoltage = divider * value
		# our return voltage is the rawVoltage x our correction factor
		returnVoltage = rawVoltage * self.correctionFactor
		return(returnVoltage)

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