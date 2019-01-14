import pickle
import socket
from threading import Thread

def send_socket_message(host, port, message):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, int(port)))
		s.sendall(pickle.dumps(message))
		# data = s.recv(1024)

class SocketServer(Thread):

	def __init__(self, port):
		Thread.__init__(self)
		self.port = port
		self.socket = None
		self.messagesIn = []
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print("Socket successfully created")
			self.socket.bind(('', int(self.port)))
			self.socket.listen(120)
			print("socket binded to %s" % (self.port))

		except socket.error as err:
			print("socket creation failed with error %s" % (err))

	def run(self):
		while True:
			self.try_get_socket_message()

	def try_get_socket_message(self):
		conn, addr = self.socket.accept()
		with conn:
			print('Connected by', addr)
			while True:
				new_data = conn.recv(1024)
				if not new_data:
					break
				self.messagesIn.append(pickle.loads(new_data))
				conn.sendall(new_data)

	def get_messagesIn(self):
		return [self.messagesIn.pop() for i in range(len(self.messagesIn))]


