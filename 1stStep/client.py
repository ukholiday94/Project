import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 8082                 # Reserve a port for your service.

s.connect((host, port))

s.send("send".encode())

check = s.recv(1024).decode()
print(check)

while True:
	if check == 'ok':
		f = open('tosend.png','rb')
		print ('Sending...')
		l = f.read(1024)
		while (l):
			s.send(l)
			l = f.read(1024)
			print ('Sending...')
		f.close()
		#s.send("endtrans".encode())
		print ("Done Sending")
		s.shutdown(socket.SHUT_WR)
		s.close		# Close the socket when done
		break
