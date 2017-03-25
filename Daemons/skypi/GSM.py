import threading
import logging
import Queue
import sys
import os
#import gammu


class GSM(object):

	def __init__(self,piManager):
		# create the object yo
		logging.debug("Create the GSM object")
		self.name = "GSM"
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
		# Register for messages
		self.piManager.register(self,"SystemTest")

	def __listener(self):
		name = threading.current_thread().getName()
		logging.debug("Running the "+name+" thread")

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




	def holder():
		temp = '''
		# Create state machine object
		sm = gammu.StateMachine()

		# Read ~/.gammurc
		sm.ReadConfig()

		# Connect to phone
		sm.Init()

		# Reads network information from phone
		netinfo = sm.GetNetworkInfo()
		netstatus = sm.GetSignalQuality()

		# Print information
		print 'Network name: %s' % netinfo['NetworkName']
		print 'Signal Strength: %s' % netstatus['SignalPercent']
		print 'Network code: %s' % netinfo['NetworkCode']
		print 'LAC: %s' % netinfo['LAC']
		print 'CID: %s' % netinfo['CID']
		'''