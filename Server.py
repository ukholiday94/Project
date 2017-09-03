import socket
import queue
import base64
import hashlib
import struct
from threading import Thread

RECV_BUFFER = 1024
PORT = 8082

que = queue.Queue()
recive_Connection = False
send_Connection = False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", PORT))
server_socket.listen(2)
print ("TCPServer Waiting for client on port 8082")

def send(client, msg):
	if(msg == "end"):
		data = bytearray([136, 0])
	else:
		data = bytearray(msg)
		if len(data) > 126:
			data = bytearray([130, 126]) + bytearray(struct.pack('>H', len(data))) + data
		else:
			data = bytearray([129, len(data)]) + data
	client.send(data)
def recv(client):
	first_byte = bytearray(client.recv(1))[0]
	FIN = (0xFF & first_byte) >> 7
	opcode = (0x0F & first_byte)
	second_byte = bytearray(client.recv(1))[0]
	mask = (0xFF & second_byte) >> 7
	payload_len = (0x7F & second_byte)
	if opcode < 3:
		if (payload_len == 126):
			payload_len = struct.unpack_from('>H', bytearray(client.recv(2)))[0]
		elif (payload_len == 127):
			payload_len = struct.unpack_from('>Q', bytearray(client.recv(8)))[0]
		if mask == 1:
			masking_key = bytearray(client.recv(4))
		masked_data = bytearray(client.recv(payload_len))
		if mask == 1:
			data = [masked_data[i] ^ masking_key[i%4] for i in range(len(masked_data))]
		else:
			data = masked_data
	else:
		return opcode, bytearray(b'\x00')
	return opcode, bytearray(data)

def sendByClient(conn): #클라이언트가 송신
	while True:
		global que
		global recive_Connection
		global send_Connection
		global filename
		global filesize
		
		if recive_Connection == True:
			send(conn,"ok".encode())
			print ("Receiving...")
			opcode, data = recv(conn)
			while True:
				if opcode == 0x8:
					print('close frame received')
					break
				que.put(data)
				opcode, data = recv(conn)
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
		global filename
		global filesize
		
		if send_Connection == True:	
			send(conn,"ok".encode())
			while (send_Connection or (not que.empty())):
				l = que.get()
				send(conn,l)
				print ("Sending...")
				print(send_Connection)
				print(que.empty())
			send(conn,"end")
			print ("Done Sending")
			recive_Connection = False
			que.queue.clear()
			conn.close()
			break
def client_thread(conn):
	global que
	global recive_Connection
	global send_Connection
	filename = ""
	filesize = ""
	
	check = conn.recv(RECV_BUFFER).decode()
	check = check[check.find("Sec-WebSocket-Key:")+19:check.find("Sec-WebSocket-Extensions:")]
	check = check.strip()
	key = check +'258EAFA5-E914-47DA-95CA-C5AB0DC85B11' 
	key = key.encode('utf-8')
	keyString = base64.b64encode(hashlib.sha1(key).digest())
	HANDSHAKE_STR = "HTTP/1.1 101 Switching Protocols\r\nUpgrade: WebSocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: "+keyString.decode('utf-8')+"\r\n\r\n"
	conn.send(HANDSHAKE_STR.encode())
	
	opcode, check = recv(conn)
	
	if opcode == 1:
		check = check.decode()
		if check == "recive": #recive
			recive_Connection = True
			reciveByClient(conn)
		elif check == "send": #send
			send_Connection = True
			sendByClient(conn)
		
while True:
	client_socket, addr = server_socket.accept()
	print ('Got connection from', addr)
	client_socket.settimeout(30)
	Thread(target=client_thread, args = (client_socket,)).start()

server_socket.close()
