import threading
import logging
import Queue
import sys
import os
import gammu


class GSM(object):

	def __init__(self,piManager):
		# create the object yo
		logging.debug("Create the GSM object")
		self.name = "GSM"
		self.piManager = piManager
		# Create the local queue
		self.Queue = Queue.PriorityQueue()
		# Connect to the phone
		self.__connecttophone()
		# Create and start the threads
		self.listenerThread = threading.Thread(target=self.__listener, name=self.name+"-listener")
		self.listenerThread.daemon = True
		self.listenerThread.start()
		self.consumerThread = threading.Thread(target=self.__queueConsumer, name=self.name+"-consumer")
		self.consumerThread.daemon = True
		self.consumerThread.start()
		# Register for messages
		self.piManager.register(self,"SystemTest")

	def __connecttophone(self):
		sm = gammu.StateMachine()
		# Read ~/.gammurc
		sm.ReadConfig()
		# Connect to phone
		sm.Init()
		self.phone = sm

	def __listener(self):
		name = threading.current_thread().getName()
		logging.debug("Running the "+name+" thread")
		folders = self.phone.GetSMSFolders()
		SMS = 
		for f in folders:
			logging.debug("Found SMS folder %s", f)
			if f.Inbox == 1:
				sms = self.phone.GetNextSMS(Folder=f,Start=True)
				print logging.debug("Got SMS %s",sms)

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

	def __sendsms(self):
		message = {
			'Text': 'python-gammu testing message',
			'SMSC': {'Location': 1},
			'Number': '+584126555508',
			}
		self.phone.SendSMS(message)

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