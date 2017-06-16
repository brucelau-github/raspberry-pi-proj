#!/usr/bin/python
import socket               # Import socket module
import sys
import time

#arg = sys.argv[1]
#host = socket.gethostyname(args) # Get local machine name
host = 'liu1ee.cs.uwindsor.ca' # Get local machine name
port = 5000

s = socket.socket()         # Create a socket object
is_connected = False
while not is_connected:
    try:
        s.connect((host, port))
        is_connected = True
    except socket.error, e:
        print 'error to connect server: ', host
        print 'retry in 5s'
        time.sleep(2)

while True:
    backstr = s.recv(1024)
    if backstr == 'bye!':
        print 'server terminates connection. Bye!'
        break
    else:
        print backstr
s.close                     # Close the socket when done
