#!/usr/bin/python

import ConfigParser
import os
import sys
import gammu

config = ConfigParser.SafeConfigParser()
try:
	config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + "/config.ini"))
except IOError:
	print "Cannot find configuration file " + os.path.dirname(os.path.abspath(__file__)) + "/config.ini"
	sys.exit(1)

for section in config.sections():
	for key in config.items(section):
		print section + " - " + key[0] + " - " + key[1]




# Create state machine object
sm = gammu.StateMachine()

# Read ~/.gammurc
sm.ReadConfig()

# Connect to phone
sm.Init()

# Reads network information from phone
netinfo = sm.GetNetworkInfo()

# Print information
print 'Network name: %s' % netinfo['NetworkName']
print 'Network code: %s' % netinfo['NetworkCode']
print 'LAC: %s' % netinfo['LAC']
print 'CID: %s' % netinfo['CID']