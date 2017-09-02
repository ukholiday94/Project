import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 8082                 # Reserve a port for your service.

s.connect((host, port))

s.send("recive".encode())

f = open('torecv.png','wb')

check = s.recv(1024).decode()
print(check)

while True:
	if check == 'ok':
		print ('Receiving...')
		l = s.recv(1024)
		while (l):
			print ('Receiving...')
			f.write(l)
			l = s.recv(1024)
		f.close()
		print ("Done Receiving")
		s.close                     # Close the socket when done
		break