# raspberry-pi-proj
## dependency
* [python 2.7](https://www.python.org)
* [Tkinter](https://wiki.python.org/moin/TkInter) - python GUI library based on Tcl
## technology
* socket
* objec oriented design
* threading
* GUI python
* message protocol
## explain

this software contains a server side and client side where all clients should connect to server
when starting up. Server could send text message or image to clients.

### server side - threadserver.py

this software contains a server side and client side where all clients should connect to server
when starting up. The server side code basicly contain three classes MessageCenter class which
inherited from MultithreadingTCPServer classes.This MessageCenter class only would send text to
clients side using send_message method. The DetailServer is another class that inherited from
MessageCenter. This class enable the server to send Message object. This DetailServer still does
not give any funtions on how to interact with Adminstators. Those interactive interface are assigned
to another class MainApp class which prints welcome message, menus and gets users inputs.

this server side include three threads - request accetping thread, interactive thread, serving thread.
To terminate server side properly without leaving zombie thread in system, it is recommend to exit
by choose option 3 in the main menu which will shutdown all background thread releasing all resources.

### client side - connector.py, appview.py, mainapp.py

the connector.py contains a classes called Connector that are related to socket communication. It
maintains socket connecting to the server, monitoring socket, handles incoming message, and shuts
it down when requested.

Class AppConnector's responsbility includes parsing incoming message into a Message Object, assembling
tcp segment, passing message to GUI.

appview.py mainly initializes an Window interface with a simple label in the middle. I would interprete
the passed Message Object showing message on interface.

There are also two thread fulfilling this client side application - socket monitoring thread, and windows
thread.

## how to run
### server side
```sh
$ cd the-project-directory
$ python threadserver.py
```
### client side
```sh
$ cd the-project-directory
$ python mainapp.py
```
