import json
import pickle
import socket
from enum import Enum
from threading import Thread

import numpy

from KafkaConsumer import consume
from MatrixFiles import readMatrixA
from KafkaProducer import init_kafka_producer, produce
from SocketServer import send_socket_message, try_get_socket_message, get_socket_server
from Tasks import TopDownTask, TaskType, TaskResponse, DownTopTask
from Worker import WorkerState, Worker

HOSTNAME = "localhost:ololo"


class Shipyard(Thread):

    def __init__(self) -> None:
        super().__init__()
        self.def_in = 0
        self.def_out = 0
        self.worker = Worker()
        self.downtop_tasks = {}
        self.host = 'localololo'
        self.port = 'portokoko'
        self.server = get_socket_server(self.host, self.port)
        self.brokers = ['ip-172-31-6-28.ec2.internal:9092',
                        'ip-172-31-11-76.ec2.internal:9092',
                        'ip-172-31-5-160.ec2.internal:9092']
        self.consumer = пуе
        self.producer = None

    def run(self):
        while True: # TODO MAKE AN ENTRY
            downtop_data = try_get_socket_message(self.server)
            [self.append_downtop_tasks(data_peace) for data_peace in downtop_data]

            if self.worker.state == WorkerState.DONE:
                self.parse_and_send_computed(self.worker.output)
                # def_in/plus def_out
                self.worker.state = WorkerState.WAITING

            if self.worker.state == WorkerState.WAITING:  # try to get and compute topdown task
                topdown_task = consume(self.consumer)
                if topdown_task is not None:
                    self.def_in += 1
                    new_downtop_awaited_task = DownTopTask(topdown_task.master_hostname,
                                                           topdown_task.master_task_id,
                                                           topdown_task.current_id,
                                                           topdown_task.tam)
                    self.downtop_tasks[topdown_task.master_task_id + topdown_task.current_id] = new_downtop_awaited_task
                    self.worker.task = topdown_task
                    self.worker.state = WorkerState.BUSY

            if self.worker.state == WorkerState.WAITING:  # try to get and compute
                for downtop_task in self.downtop_tasks:
                    if downtop_task.is_complete():
                        self.downtop_tasks.pop(downtop_task)
                        self.worker.task = downtop_task
                        self.worker.state = WorkerState.BUSY

    def parse_and_send_computed(self, output):
        if output.task_type == TaskType.TOPDOWN:
            if type(output) == list:
                [self.send_topdown_task(task) for task in output]
            else:
                self.send_downtop_responce(output)  # LEAF
        elif output.task_type == TaskType.DOWNTOP:
            self.send_downtop_responce(output)

    def send_topdown_task(self, task):
        self.def_out += 1
        task.hostname = HOSTNAME
        produce(self.producer, task)

    def send_downtop_responce(self, responce):
        self.def_in -= 1
        send_socket_message(responce.host, responce.port, responce)  # TODO DIVIDE HOSTNAME

    def append_downtop_tasks(self, data):
        if data['task_id'] not in self.downtop_tasks:
            pass
        data['task_id'].p_matrices[data['p_id']] = data['matrix']
        self.def_out -= 1  # Would be nice to have a transaction
