import threading
import logging
import Queue
import sys
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

class Manager(object):

	def __init__(self):
		# create the object yo
		logging.debug("Create the Manager object")
		self.name = "Manager"
		# Create the local queue
		self.Queue = Queue.PriorityQueue()
		self.Registrations = []
		# Create and start the threads
		self.consumerThread = threading.Thread(target=self.__queueConsumer, name=self.name+"-consumer")
		self.consumerThread.daemon = True
		self.consumerThread.start()

	def addToQueue(self,event,priority=99):
		self.Queue.put( (priority,event) ) 
		
	def __queueConsumer(self):
		name = threading.current_thread().getName()
		logging.debug("Running the "+name+" thread")
		# process queue objects as the come in run the thread forever
		while 1:
			item = self.Queue.get(True)
			event = item[1].getTask()
			logging.debug("Route Queue Item %s", event)
			for reg in self.Registrations:
				if reg[1] == event:
					logging.debug("Routing %s to Module %s", event, reg[0].name)
					reg[0].addToQueue(item[1],priority=item[0])
			self.Queue.task_done()
			
	def register(self,queue,event):
		reg = (queue,event)
		try:
			self.Registrations.index(reg)
			logging.debug("Module %s has already registered for %s", queue.name, event)
		except ValueError:
			logging.debug("Module %s has registered for %s", queue.name, event)
			self.Registrations.append( (queue,event) )
		return(0)
		
	def deregister(self,queue,event):
		reg = (queue,event)
		try:
			self.Registrations.remove( (queue,event) )
			logging.debug("Module %s has deregistered for %s", queue.name, event)
		except ValueError:
			logging.debug("Module %s is not registered for %s", queue.name, event)
		return(0)



class Event(object):	

	def __init__(self,task,args):
		self.args = args
		self.task = task
		self.additionalargs = {}

	def setadditionalarg(self,name,value):
		self.additionalargs[name] = value

	def getadditionalarg(self,name):
		return(self.additionalargs[name])

	def getTask(self):
		return(self.task)

	def getargs(self):
		return(self.args)
