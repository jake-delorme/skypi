import threading
import logging
import queue
import sys
import os


class Camera(object):

	def __init__(self):
		# create the object yo