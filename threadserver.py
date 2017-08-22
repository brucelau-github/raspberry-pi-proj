#!/usr/bin/python
import threading
import SocketServer
import socket
from message import Message, TextMessage, ImageMessage

class MessageCenter(SocketServer.ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass)
        self.clients = []

    def process_request_thread(self, request, client_address):
        """Same as in ThreadmingMixin but overwrite here.

        In addition, exception handling is done here.

        """
        try:
            self.clients.append(request)
            self.finish_request(request, client_address)
        except:
            self.handle_error(request, client_address)
            self.shutdown_request(request)
    def send_message(self, message=""):
        """Send message to all clients
        default send empty message
        """
        if not self.clients:
            print "No Clients"
            return
        for client in self.clients:
            try:
                print "send messge to {}".format(client.getpeername())
                client.sendall(message)
            except socket.error as e:
                client.close()
                print("client colsed due to {}".format(e))
                self.clients.remove(client) #connect closed


class MessageHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print 'Got connection from {}'.format(self.client_address)
        txtmsg = TextMessage()
        txtmsg.set_text_body("hello guest!")
        self.request.sendall(txtmsg.as_string())


class DetailServer(MessageCenter):
    """inheritate from MessageCenter
    over write send_message with MessageObject
    """
    def send_message(self, message=None):
        """Overwite Send message to all clients
        default send empty message
        """
        if not self.clients:
            print "No Clients"
            return
        if not isinstance(message, Message):
            print "not a Message Class"
            return
        for client in self.clients:
            try:
                print "send messge to {}".format(client.getpeername())
                client.sendall(message.as_string())
            except socket.error as e:
                client.close()
                print("client colsed due to {}".format(e))
                self.clients.remove(client) #connect closed


def get_input(server):
    while True:
        message = raw_input("Enter your message here:")
        if message is None:
            server.send_message("")
        server.send_message(message)

def get_message_input(server):
    while True:
        message = raw_input("Enter your message here:")
        txtmsg = TextMessage()
        txtmsg.set_text_body(message)
        server.send_message(txtmsg.as_string())

def get_image_input(server):
    while True:
        message = raw_input("choose the image you want to send:")
        imgmsg = ImageMessage()
        imgmsg.load_from_filepath(filepath="test-image.jpg")
        server.send_message(imgmsg)

def thread_input(server):
    """Start a new thread to process the request."""
    t = threading.Thread(target = get_image_input, args=(server,))
    t.daemon = True
    t.start()

if __name__ == "__main__":

    HOST, PORT = "0.0.0.0", 5000
    #server = MessageCenter((HOST, PORT), MessageHandler)
    server = DetailServer((HOST, PORT), MessageHandler)
    thread_input(server)
    print 'server running on port {0}'.format(server.server_address)
    server.serve_forever()
