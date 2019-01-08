import json
import pickle
import socket
from enum import Enum
from threading import Thread

import numpy

from MatrixFiles import readMatrixA
from KafkaProducer import init_kafka_producer, publish_message
from SocketServer import send_socket_message
from Tasks import TopDownTask, TaskType, TaskResponse
from Worker import WorkerState, Worker

HOSTNAME = "localhost:ololo"

class Shipyard(Thread):
	
	
	
	def __init__(self) -> None:
		super().__init__()
		self.def_in = 0
		self.def_out = 0
		self.worker = Worker()
		self.downtop_tasks = None
		self.server = None
		self.consumer = None
		self.producer = None
	
	def run(self):
		while True:
			downtop_data = self.try_get_socket_message()
			[self.append_downtop_tasks(data_peace) for data_peace in downtop_data]  # TODO Control
			
			if self.worker.state == WorkerState.DONE:
				self.parse_and_send_computed(self.worker.output)  # TODO  to top(socket) and down(produce) + minus def_in/plus def_out
				self.worker.state = WorkerState.WAITING
			
			if self.worker.state == WorkerState.WAITING: # try to get and compute topdown task
				topdown_data = self.consumer.try_to_consume() # TODO
				if topdown_data is not None:
					self.def_in += 1
					self.worker.task = TopDownTask(topdown_data) # TODO + plus defin
					self.worker.state = WorkerState.BUSY
			
			if self.worker.state == WorkerState.WAITING: # try to get and compute
				for downtop_task in self.downtop_tasks:
					if downtop_task.is_complete():  #  TODO
						self.downtop_tasks.pop(downtop_task)
						self.worker.task = downtop_task  # TODO
						self.worker.state = WorkerState.BUSY
					
					
				
	def parse_and_send_computed(self, output):
		if output.task_type == TaskType.TOPDOWN:
			if type(output) == list:
				self.handle_next_topdown_tasks(tasks)
			else:
				self.send_leaf_responce(output)
		elif output.task_type == TaskType.DOWNTOP:
			response = TaskResponse(output) # TODO
			self.send_downtop_responce(response) # TODO
	
	def handle_next_topdown_tasks(self, tasks):
		[self.send_topdown_task(task) for task in tasks]
         # TODO add downtop waiting task
        self.downtop_tasks

			
	def send_topdown_task_output(self, output):
		if type(output) == list:
			for new_topdown_task in output:
				self.send_topdown_task(new_topdown_task)
		else:
			output
			
		


	def send_topdown_task(self, task):
		self.def_out += 1
		task.hostname = HOSTNAME
		self.producer.produce(task)


	def send_downtop_responce(self, responce):
		self.def_in -= 1
		send_socket_message(responce.hostname, responce) # TODO DIVIDE HOSTNAME
 
 
 
	
	def append_downtop_tasks(self, data):
		if data['task_id'] not in self.downtop_tasks:
			pass
		data['task_id'].p_matrices[data['p_id']] = data['matrix']
		self.def_out -= 1  # Would be nice to have a transaction


matrix = readMatrixA()
matrix_data_type = matrix.dtype.name
matrix_shape = matrix.shape

pickled = pickle.dumps(matrix)
print(pickled)
unpickled = pickle.loads(pickled)

print(unpickled)


# json_dump = json.dumps({'matrix': matrix.pickle(), 'shape': matrix_shape, 'data_type': matrix_data_type})
#
# producer = init_kafka_producer()
# # publish_message(producer, 'test', json_dump)


def encode_matrix(matrix):
	return matrix.tobytes()


def decode_matrix(matrix_bytes, matrix_data_type, matrix_shape):
	return numpy.frombuffer(matrix_bytes, dtype=matrix_data_type).reshape(matrix_shape)
