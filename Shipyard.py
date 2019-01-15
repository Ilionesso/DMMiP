
import atexit
from threading import Thread


from KafkaConsumer import consume, init_kafka_consumer
from KafkaProducer import init_kafka_producer, produce
from SocketServer import SocketServer, send_socket_message
from Tasks import TaskType, DownTopTask, EntryTask
from Worker import WorkerState, Worker

class Shipyard(Thread): # make a singletone?

    def __init__(self, host, port):
        Thread.__init__(self)
        self.def_in = 0
        self.def_out = 0
        self.worker = Worker()
        self.worker.start()
        self.downtop_tasks = {}
        self.host = host
        self.port = port
        self.server = SocketServer(self.port)
        self.consumer = init_kafka_consumer()
        self.producer = init_kafka_producer()

    def run(self):
        while True:

            print("check for downtop responces")
            downtop_data = self.server.get_messagesIn()
            if downtop_data:
                [self.append_downtop_tasks(data_peace) for data_peace in downtop_data]

            if self.worker.state == WorkerState.DONE:
                print("check for done tasks")
                self.parse_and_send_computed(self.worker.output)
                # def_in/plus def_out
                self.worker.state = WorkerState.WAITING

            if self.worker.state == WorkerState.WAITING:  # try to get and compute topdown task
                print("check for topdown tasks")
                topdown_task = consume(self.consumer)
                if topdown_task is not None:
                    print("got a topdown task" + topdown_task.master_task_id + topdown_task.current_id)
                    self.def_in += 1
                    new_downtop_awaited_task = DownTopTask(topdown_task.master_host,
                                                           topdown_task.master_port,
                                                           topdown_task.master_task_id,
                                                           topdown_task.current_id)
                    self.downtop_tasks[topdown_task.master_task_id + topdown_task.current_id] = new_downtop_awaited_task
                    self.worker.task = topdown_task
                    self.worker.state = WorkerState.BUSY

            if self.worker.state == WorkerState.WAITING:
                print("check for downtop tasks")  # try to get and compute downtop tasks
                for downtop_task_num, downtop_task in self.downtop_tasks.items():
                    if downtop_task.is_complete():
                        print("downtop task " + downtop_task_num + " is complete")
                        self.downtop_tasks.pop(downtop_task)
                        self.worker.task = downtop_task
                        self.worker.state = WorkerState.BUSY
                    else:
                        print("downtop task " + downtop_task_num + " is NOT complete")

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
        task.master_hostname = self.host
        produce(self.producer, task)

    def send_downtop_responce(self, responce):
        self.def_in -= 1
        send_socket_message(responce.host, responce.port, responce)

    def append_downtop_tasks(self, data):
        if data['task_id'] not in self.downtop_tasks:
            pass
        data['task_id'].p_matrices[data['p_id']] = data['matrix']
        self.def_out -= 1  # Would be nice to have a transaction

    def compute_entry(self):
        entry_task = EntryTask()
        output = entry_task.compute()
        if type(output) == list:
            self.downtop_tasks[0] = DownTopTask('', '', '', 0)
            [self.send_topdown_task(task) for task in output]


    # @atexit.register
    # def cleanup(self):
    #     self.server.close()


