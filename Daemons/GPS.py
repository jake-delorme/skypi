import threading
import logging
import Queue
import sys
import os


class GPS(object):

	def __init__(self):
		# create the object yo
		logging.debug("Create the GPS object")