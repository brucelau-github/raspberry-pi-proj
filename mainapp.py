from window import App
from client import Connector
import threading

cli = Connector()
cli.connect()
win_app = App()
t = threading.Thread(target=cli.getmsg, args=(win_app,))
t.start()
print "ad"
win_app.run()
win_app.close()
