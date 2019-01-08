from enum import Enum
from threading import Thread


class WorkerState(Enum):
	WAITING = 0
	BUSY = 1
	DONE = 2

class Worker(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.state = WorkerState.WAITING
		self.task = None
		self.output = None
		# make shipyard a singletone/bind a worker to a single shipyard/do nothing
		
	def run(self):
		while True:
			if self.state is WorkerState.BUSY:
				self.output = self.task.compute()
				self.state = WorkerState.DONE
