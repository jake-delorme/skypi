import threading
import logging
import Queue
import sys
import os
#import gammu


class GSM(object):

	def __init__(self):
		# create the object yo
		logging.debug("Create the GSM object")



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