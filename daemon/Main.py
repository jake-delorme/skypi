#!/usr/bin/python

import ConfigParser
import os

scriptpath = os.path.dirname(__file__)


config = ConfigParser.SafeConfigParser()
try:
	config.read(scriptpath + "/../config.ini", "config.ini")
except ConfigParser.Error:
	print "Caught an error YO"
