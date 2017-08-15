#!/usr/bin/python
import socket               # Import socket module
import sys
import threading
import select


class Connector:

    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.skt = socket.socket()
        self.is_connected = False
        self.request_shutdown = False
        self.connect()

    def fileno(self):
        """Return socket file number.
        Interface required by select().
        """
        return self.skt.fileno()

    def connect(self):
        try:
            self.skt.connect((self.host, self.port))
            self.is_connected = True
        except socket.error as socketerror:
            print 'error to connect server: {0}'.format(self.host)
            raise socketerror 

    def getmsg(self):
        data = self.skt.recv(1024)
        return data

    def disconnect(self):
        self.is_connected = False
        self.skt.close()

    def serve_forever(self, poll_interval=0.5):
        """Monitor message coming from the socket

        Polls for shutdown every poll_interval seconds. Ignores
        self.timeout. If you need to do periodic tasks, do them in
        another thread.
        """
        try:
            while not self.request_shutdown:
                r, w, e = select.select([self], [], [], poll_interval)
                if self in r:
                    self.handle_message()
        finally:
            self.disconnect()

    def handle_message(self):
        """overwrite by sub class
        consume the message
        """
        pass


class AppConnector(Connector):
    """App specified connector
    pass message to app
    """
    def __init__(self, host='localhost', port=5000, app=None):
        Connector.__init__(self, host, port)
        self.app = app

    def handle_message(self):
        self.app.update_msg(self.getmsg())


if __name__ == '__main__':
    c = Connector()
    c.getmsg()
