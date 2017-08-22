#!/usr/bin/python
import socket               # Import socket module
import sys
import threading
import select
import message


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
        self.moredata = False
        self.msg = None

    def handle_message(self):
        self.parse_message()

    def parse_message(self):
        raw_data = self.getmsg()
        if self.moredata:
            self.assemble_data(raw_data)
        else:
            self.msg = None #clear data before assign new data
            self.msg = message.Message()
            self.msg.parse_fromstr(raw_data)
            if len(self.msg._body) == self.msg.get_body_length():
                self.moredata = False
                self.update_app()
            else:
                self.moredata = True
    def assemble_data(self, data):
        self.msg.append_body(data)
        if len(self.msg._body) < self.msg.get_body_length():
            self.moredata = True
        elif len(self.msg._body) == self.msg.get_body_length():
            self.moredata = False
            self.update_app()
        else: #got some addtional noisy data so get rid of all the data
            self.msg = None
            self.moredata = False

    def update_app(self):
        if self.msg.is_image():
            imgmsg = message.ImageMessage()
            imgmsg.parse_fromobj(self.msg)
            self.app.update_image(imgmsg)
        else:
            txtmsg = message.TextMessage()
            txtmsg.parse_fromobj(self.msg)
            self.app.update_msg(txtmsg)

if __name__ == '__main__':
    c = Connector()
    c.getmsg()
