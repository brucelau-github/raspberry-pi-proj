#!/usr/bin/python
import socket               # Import socket module
class Server:
    def __init__(self):
        self.s = socket.socket()         # Create a socket object
        self.host = socket.gethostname() # Get local machine name
        self.port = 5000                 # Reserve a port for your service.
        self.s.bind((host, port))        # Bind to the port
        self.s.listen(5)                 # Now wait for client connection.
        print 'server running on port {0}'.format(port)

    def serve(self):
        while True:
            c, addr = s.accept()     # Establish connection with client.
            print 'Got connection from', addr
            while True:
                print 'enter your message:'
                msg = raw_input()
                if msg == 'bye!':
                print msg
                c.send(msg)
                break
                    else:
                    c.send(msg)
                print 'waiting for another client'

                c.close()                # Close the connection
