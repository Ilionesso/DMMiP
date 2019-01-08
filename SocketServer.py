import pickle
import socket


def get_socket_server(port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Socket successfully created")
		s.bind(('localhost', int(port)))
		s.listen()
		print("socket binded to %s" % (port))
	except socket.error as err:
		print("socket creation failed with error %s" % (err))

def try_get_socket_message(server):
	conn, addr = server.accept()
	with conn:
		print('Connected by', addr)
		data = []
		while True:
			new_data = conn.recv(1024)
			if not data:
				break
			data.append(pickle.loads(new_data))
			conn.sendall(data)
		return data
	
def send_socket_message(host, port, message):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, int(port)))
		s.sendall(pickle.dumps(message))
		data = s.recv(1024)
