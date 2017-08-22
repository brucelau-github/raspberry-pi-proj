import unittest
import threading
import re
import message
import StringIO
from connector import Connector, AppConnector
import SocketServer
from threadserver import DetailServer
from datetime import datetime
from PIL import Image


class App:
    def update_msg(self, txtmsg):
        print txtmsg.get_body()
        return txtmsg
    def update_image(self, imgmsg):
        img = imgmsg.get_image()
        img.show()
        return imgmsg


class ConnectorTest(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.c = AppConnector(app=self.app)

    def test_header(self):
        c = self.c
        c.serve_forever()


if __name__ == '__main__':
    unittest.main()
