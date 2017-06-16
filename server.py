#!/usr/bin/python
import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 5000                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
print 'server running on port {0}'.format(port)
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   while True:
        print 'enter your message:'
        msg = raw_input()
        if msg == 'bye!':
            break
        else:
            c.send(msg)

   c.close()                # Close the connection
