#!/usr/bin/python
import socket               # Import socket module
import sys
import threading

SOCKET_TIMEOUT = 1.0

class Connector:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.skt = socket.socket()         # Create a socket object
        self.skt.settimeout(SOCKET_TIMEOUT)
        self.is_connected = False
        self.shutdown = False
    def connect(self):
        try:
            self.skt.connect((self.host, self.port))
            self.is_connected = True
        except socket.error, e:
            return 'error to connect server: {0}'.format(self.host)
    def getmsg(self, win_app):
        while not self.shutdown:
            try:
                backstr = self.skt.recv(1024)
                if  backstr == 'bye!':
                    win_app.updatemsg('server terminates connection. Bye!')
                    break
                else:
                    win_app.updatemsg(backstr)
            except socket.timeout:
                pass

    def disconnect(self):
        self.skt.close()
