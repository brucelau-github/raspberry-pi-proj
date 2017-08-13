#!/usr/bin/python
import threading
import SocketServer              # Import socket module

class MessageHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print 'Got connection from {}'.format(self.client_address)
        response = "hello world:\n"
        self.request.sendall(response)
        self.request.close()
    def get_input(self):
        return raw_input("Enter your message:")
if __name__ == "__main__":

    HOST, PORT = "0.0.0.0", 5000
    server = SocketServer.ThreadingTCPServer((HOST, PORT), MessageHandler)
    print 'server running on port {0}'.format(server.server_address)
    server.serve_forever()
