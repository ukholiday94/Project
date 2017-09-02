import socket
import queue
from threading import Thread

RECV_BUFFER = 1024
PORT = 8082

que = queue.Queue()
recive_Connection = False
send_Connection = False

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
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("", PORT))
	server_socket.listen(2)
	print ("TCPServer Waiting for client on port 8082")

	client_socket, addr = server_socket.accept()
	print ('Got connection from', addr)
	Thread(target=client_thread, args = (client_socket,)).start()

server_socket.close()

'''
import socket
import queue
import time
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
			data = conn.recv(1024)
			while (data):
				que.put(data)
				print("1st")
				data = conn.recv(1024)
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
			print ("Sending...")
			while (send_Connection or (not que.empty())):
				l = que.get()
				print("2nd")
				conn.send(l)
				print ("Sending...")
			conn.shutdown(socket.SHUT_WR)
			print ("Done Sending")
			recive_Connection = False
			conn.close()
			break
def client_thread(conn):
	global que
	global recive_Connection
	global send_Connection
	check = conn.recv(1024).decode()
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


from threading import Thread

while True:
	conn, addr = soc.accept()
	ip, port = str(addr[0]), str(addr[1])
	print('Accepting connection from ' + ip + ':' + port)
	try:
		Thread(target=client_thread, args=(conn, ip, port)).start()
	except:
		print("Terible error!")
		import traceback
		traceback.print_exc()
soc.close()

def do_some_stuffs_with_input(input_string):  
	"""
	This is where all the processing happens.

	Let's just read the string backwards
	"""

	print("Processing that nasty input!")
	return input_string[::-1]

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):

	# the input is in bytes, so decode it
	input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

	# MAX_BUFFER_SIZE is how big the message can be
	# this is test if it's sufficiently big
	import sys
	siz = sys.getsizeof(input_from_client_bytes)
	if	siz >= MAX_BUFFER_SIZE:
		print("The length of input is probably too long: {}".format(siz))

	# decode input and strip the end of line
	input_from_client = input_from_client_bytes.decode("utf8").rstrip()

	res = do_some_stuffs_with_input(input_from_client)
	print("Result of processing {} is: {}".format(input_from_client, res))

	vysl = res.encode("utf8")  # encode the result string
	conn.sendall(vysl)	# send it to client
	conn.close()  # close connection
	print('Connection ' + ip + ':' + port + " ended")


while 1:
	read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,CONNECTION_LIST,[],60)
 
	for sock in read_sockets:
		#New connection
		if sock == server_socket:
			# Handle the case in which there is a new connection recieved through server_socket
			sockfd, addr = server_socket.accept()
			CONNECTION_LIST.append(sockfd)
			print "Client (%s, %s) connected" % addr
		 
		#Some incoming message from a client
		else:
			# Data recieved from client, process it
			try:
				#In Windows, sometimes when a TCP program closes abruptly,
				# a "Connection reset by peer" exception will be thrown
				data = sock.recv(RECV_BUFFER)
				if data:
					broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)				
			 
			except:
				broadcast_data(sock, "Client (%s, %s) is offline" % addr)
				print "Client (%s, %s) is offline" % addr
				sock.close()
				CONNECTION_LIST.remove(sock)
				continue
	
server_socket.close()


while 1:
	client_socket, address = server_socket.accept()
	print ("I got a connection from ", address)
	while 1:
		data = input('SEND( TYPE q or Q to Quit):')
		if(data == 'Q' or data == 'q'):
			client_socket.send (data.encode())
			client_socket.close()
			break;
		else:
			# 데이터 클라이언트로 송신
			client_socket.send(data.encode())
		
		data = client_socket.recv(4294967296).decode()
		if(data == 'q' or data == 'Q'):
			client_socket.close()
			break;
		else:
			print ("RECEIVED:" , data)
	break;
server_socket.close()
print("SOCKET closed... END")


TCP Client Code:
# TCP client example
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("www.hsd.or.kr", 5000))
while 1:
	data = client_socket.recv(512).decode()
	if ( data == 'q' or data == 'Q'):
		client_socket.close()
		break;
	else:
		print ("RECEIVED:" , data)
		data = input ( "SEND( TYPE q or Q to Quit):" )
		if ( data == 'q' or data == 'Q'):
			client_socket.send(data.encode())
			client_socket.close()
			break;
		else:
			client_socket.send(data.encode())
print ("socket colsed... END.")
'''
