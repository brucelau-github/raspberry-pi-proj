#!/usr/bin/python
import threading
import SocketServer
import os
import socket
import textwrap
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
            print "There are no connected Clients"
            print "Operation Cancelled"
            return
        for client in self.clients:
            try:
                print "send messge to {}".format(client.getpeername())
                client.sendall(message)
            except socket.error as e:
                client.close()
                print("client colsed due to {}".format(e))
                self.clients.remove(client) #connect closed

    def close_clients(self):
        for client in self.clients:
            client.close()


    def shutdown(self):
        """
        shutdown all client connect first, then shutdown server
        """
        self.close_clients()
        SocketServer.ThreadingTCPServer.shutdown(self)


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
            print "There are no connected Clients"
            print "Operation Cancelled"
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

class MainApp:
    def __init__(self, host="0.0.0.0", port=5000):
        self.server = DetailServer((host, port), MessageHandler)
        self.thread_server()
        self.mainthread = threading.currentThread()
        self.width = 72
        self.keep_run = True

    def get_input(self, server):
        while True:
            message = raw_input("Enter your message here:")
            if message is None:
                server.send_message("")
            server.send_message(message)

    def send_text_msg(self):
        self.clear_screen()
        self.print_line("#")
        self.print_bold("Text Edit Mode")
        self.print_dotline()
        self.print_wrapmsg("Instruction: Enter/Paste your content at bellow. Ctrl-D to send it.")
        self.print_dotline()
        contents = []
        while True:
            try:
                line = raw_input("")
            except EOFError:
                break
            contents.append(line)
        text = "\n".join(contents)
        self.print_dotline()
        self.print_line("=")
        print("server status...")
        txtmsg = TextMessage()
        txtmsg.set_text_body(text)
        self.server.send_message(txtmsg)
        self.print_line("#")
        self.pasue_screen()

    def send_image_msg(self):
        self.clear_screen()
        self.print_line("#")
        self.print_bold("Image Selection Mode")
        self.print_dotline()
        self.print_wrapmsg("choose the image you want to send:")
        self.print_dotline()
        filename = self.choose_image()
        self.print_line("=")
        print("server status...")
        if filename:
            imgmsg = ImageMessage()
            imgmsg.load_from_filepath(filepath=filename)
            self.server.send_message(imgmsg)
        else:
            print("no file selected")
        self.print_line("#")
        self.pasue_screen()

    def choose_image(self):
        here = os.path.dirname(os.getcwd())
        imgfiles = []
        errormsg = ''
        for fn in os.listdir(os.getcwd()):
            if fn.endswith(".jpg"):
                imgfiles.append(fn)
        filenos = len(imgfiles)
        if not imgfiles:
            return None
        while True:
            self.print_dotline()
            for idx, fn in enumerate(imgfiles,start=1):
                print("{}. {}".format(idx,fn))
            self.print_dotline()
            if errormsg:
                print(errormsg)
                self.print_dotline()
            opt = raw_input("Choose your file from the list to send:")
            try:
                opt = int(opt)
            except ValueError as e:
                errormsg = "Invalid input, args: {} \n".format(e.args)
                continue
            if opt < 1 or opt > (filenos + 1) :
                errormsg = "Invalid input, args: {} \n".format(opt)
                errormsg +="Number should be in the range 1-{}. Try again".format(filenos)
                continue
            else:
                break
        return imgfiles[opt-1]


    def thread_server(self):
        """Start a new thread to process the request."""
        self.serverthread = threading.Thread(target = self.server.serve_forever)
        self.serverthread.daemon = True
        self.serverthread.start()

    def print_dotline(self):
        self.print_line()

    def print_line(self, char="-"):
	dotted_line = char * self.width
	print(dotted_line)

    def print_welcome(self):
        self.clear_screen()
        self.print_dotline()
	self.print_bold("Welcome to Raspi Message Center V 1.0.1:")
        msg = (
                "This application enables you to send an text or image message to "
                "all connected raspiberry pi clients. All the message willl show "
                "up on clients screen. "
                "In order to use it properly, You could press enter to popup main "
                "menu, then you can choose what option you want. "
                "Enjoy your application!"
              )
        self.print_wrapmsg(msg)
        self.print_dotline()
        raw_input("press any key or enter to start ...")

    def pasue_screen(self):
        raw_input("press any key or enter to continue ...")

    def print_bold(self, msg=''):
	print("\033[1m{}\033[0m".format(msg))

    def print_wrapmsg(self, msg=''):
        print(textwrap.fill(msg, width=self.width))

    def print_menu(self, errormsg=''):
        self.clear_screen()
        self.print_dotline()
        self.print_bold("Main Menu")
        self.print_dotline()
        print(" 1. send a text message")
        print(" 2. send a image message")
        print(" 3. shut down server")
        print(" 0. exit to welcome screen")
        self.print_dotline()
        if errormsg:
            print(errormsg)
            self.print_dotline()

    def clear_screen(self):
        print('\033[H\033[J')

    def shutdown(self):
        self.server.shutdown()
        self.serverthread.join()
        self.keep_run = False

    def get_user_option(self):
        opt = ""
        errormsg = ''
        while True:
            self.print_menu(errormsg)
            opt = raw_input("Choose your option to start:")
            try:
                opt = int(opt)
            except ValueError as e:
                errormsg = "Invalid input, args: {} \n".format(e.args)
                continue
            if opt < 0 or opt > 4 :
                errormsg = "Invalid input, args: {} \n".format(opt)
                errormsg +="Number should be in the range 1-4. Try again"
                continue
            else:
                break
        return opt

    def main(self):
        options = {
                1:'send_text_msg',
                2:'send_image_msg',
                3:'shutdown',
                0:'print_welcome'
                }
        self.print_welcome()
        while  self.keep_run:
            self.clear_screen()
            opt = self.get_user_option()
            method = getattr(self, options[opt])
            method()


if __name__ == "__main__":
    app = MainApp()
    app.main()
