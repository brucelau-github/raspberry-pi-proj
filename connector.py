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
        self.request_shutdown = False
        self.connect()

    def connect(self):
        try:
            self.skt.connect((self.host, self.port))
            self.is_connected = True
        except socket.error as socketerror:
            print 'error to connect server: {0}'.format(self.host)
            raise socketerror 
    def getmsg(self):
        while not self.request_shutdown:
            try:
                backstr = self.skt.recv(1024)
                if backstr:
                    print(backstr)
            except socket.timeout:
                print("recv timeout")
            except socket.error:
                self.disconnect()
                print("socket disconnected")
                break

    def disconnect(self):
        self.skt.close()
if __name__ == '__main__':
    c = Connector()
    c.getmsg()
