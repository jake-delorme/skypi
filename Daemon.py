#!/usr/bin/python

import ConfigParser
import os
import sys
import serial

config = ConfigParser.SafeConfigParser()
try:
	config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + "/../config.ini"))
except IOError:
	print "Cannot find configuration file " + os.path.dirname(os.path.abspath(__file__)) + "/../config.ini"
	sys.exit(1)

for section in config.sections():
	for key in config.items(section):
		print section + " - " + key[0] + " - " + key[1]


try:
	gsm = serial.Serial(
		port=config.get('GSM','port'),
		baudrate=config.get('GSM','baudrate'))
except ValueError:
	print "Invalid parameters for Serial port"
	sys.exit(1)
except serial.SerialException:
	print "Cannot open serial port"
	sys.exit(1)
