"""Manages the battery readings and battery messages"""
import threading
import logging
import Queue
import time
from Manager import Event
from gpiozero import MCP3008


class Battery(object):

	def __init__(self, piManager, vref=3.3, r1=51000, r2=6800, correctionFactor=1):
		# create the object yo
		logging.debug("Create the Battery object")
		self.name = "Battery"
		self.piManager = piManager
		# Create the local queue
		self.Queue = Queue.PriorityQueue()
		# The voltage mathing
		self.vref = vref
		self.r1 = r1
		self.r2 = r2
		self.correctionFactor = correctionFactor
		# Create and start the threads
		self.listenerThread = threading.Thread(target=self.__listener, name=self.name+"-listener")
		self.listenerThread.daemon = True
		self.listenerThread.start()
		self.consumerThread = threading.Thread(target=self.__queueConsumer, name=self.name+"-consumer")
		self.consumerThread.daemon = True
		self.consumerThread.start()
		# Register for messages
		self.piManager.register(self, "SystemTest")

	def __listener(self):
		name = threading.current_thread().getName()
		logging.debug('Running the %s thread', name)
		while True:
			voltage = self.__calculateBatteryVoltage()
			logging.info('Battery voltage is %s', voltage)
			time.sleep(5)

	def __calculateBatteryVoltage(self):
		# The ratio the divider is dropping our voltage by
		divider = (self.r1 + self.r2) / float(self.r2)
		# expand the value read from 0 - 1 back to its real value based on vref
		adc = MCP3008(0)
		val = adc.value
		rval = adc.raw_value
		logging.debug('Read %s from MCP3008 (raw=%s)', val, rval)
		value = val * self.vref
		# the output voltage is the divider * the value
		rawVoltage = divider * value
		# our return voltage is the rawVoltage x our correction factor
		returnVoltage = rawVoltage * self.correctionFactor
		return returnVoltage

	def addToQueue(self, event, priority=99):
		self.Queue.put((priority, event))

	def __queueConsumer(self):
		name = threading.current_thread().getName()
		logging.debug("Running the "+name+" thread")
		# process queue objects as the come in run the thread forever
		while 1:
			item = self.Queue.get(True)
			task = item[1].getTask()
			logging.debug("Process Queue task "+task)
