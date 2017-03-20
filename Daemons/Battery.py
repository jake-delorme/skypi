import threading
import logging
import Queue
import sys
import os


class Battery(object):

	def __init__(self):
		# create the object yo
		logging.debug("Create the Battery object")