import socket


def get_socket_server():
	HOST = '127.0.0.1'
	PORT = 65432
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		return s

def try_get_socket_message(server):
	conn, addr = server.accept()
	with conn:
		print('Connected by', addr)
		data = []
		while True:
			new_data = conn.recv(1024)
			if not data:
				break
			data.append(new_data)
			conn.sendall(data)
		return data
	
def send_socket_message(host, port, message):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, port))
		s.sendall(message)
		data = s.recv(1024)
