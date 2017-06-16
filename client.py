#!/usr/bin/python
import socket               # Import socket module
import sys

#arg = sys.argv[1]
#host = socket.gethostyname(args) # Get local machine name
host = 'liu1ee.cs.uwindsor.ca' # Get local machine name
port = 5000

s = socket.socket()         # Create a socket object
s.connect((host, port))

while True:
    backstr = s.recv(1024)
    if backstr == 'bye!':
        break
    else:
        print backstr
s.close                     # Close the socket when done
