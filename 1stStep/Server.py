import socket
import queue
from threading import Thread

RECV_BUFFER = 1024
PORT = 8082

que = queue.Queue()
recive_Connection = False
send_Connection = False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", PORT))
server_socket.listen(2)
print ("TCPServer Waiting for client on port 8082")

def sendByClient(conn): #클라이언트가 송신
	while True:
		global que
		global recive_Connection
		global send_Connection
		if recive_Connection == True:
			conn.send("ok".encode())
			print ("Receiving...")
			data = conn.recv(RECV_BUFFER)
			while (data):
				que.put(data)
				data = conn.recv(RECV_BUFFER)
				print ("Receiving...")
			print ("Done Receiving")
			send_Connection = False
			conn.close()
			break
def reciveByClient(conn): #클라이언트가 수신
	while True:
		global que
		global recive_Connection
		global send_Connection
		if send_Connection == True:	
			conn.send("ok".encode())
			while (send_Connection or (not que.empty())):
				l = que.get()
				conn.send(l)
				print ("Sending...")
			conn.shutdown(socket.SHUT_WR)
			print ("Done Sending")
			recive_Connection = False
			que.queue.clear()
			conn.close()
			break
def client_thread(conn):
	global que
	global recive_Connection
	global send_Connection
	check = conn.recv(RECV_BUFFER).decode()
	if check == "recive": #recive
		recive_Connection = True
		reciveByClient(conn)
	elif check == "send": #send
		send_Connection = True
		sendByClient(conn)
		
while True:
	client_socket, addr = server_socket.accept()
	print ('Got connection from', addr)
	Thread(target=client_thread, args = (client_socket,)).start()

server_socket.close()