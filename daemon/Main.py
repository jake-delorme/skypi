#!/usr/bin/python

import ConfigParser
import os


config = ConfigParser.SafeConfigParser()
try:
	config.readfp(os.path.dirname(__file__) + "config.ini")
except ConfigParser.Error:
	print "Caught an error YO"
