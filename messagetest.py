import unittest
import message
from datetime import datetime

class MessageTest(unittest.TestCase):

    def setUp(self):
        self.msg = message.Message()

    def test_getheader(self):
        msg = self.msg
        msg.set_header(message.FROM, "liu1ee@uwindsor.ca")
        self.assertTrue("From: liu1ee@uwindsor.ca" in msg.get_header())
        msg.set_header(message.FROM, "liuee@uwindsor.ca")
        self.assertTrue("From: liuee@uwindsor.ca" in msg.get_header())
        msg.set_header(message.TO, "liu1ee@uwindsor.ca")
        self.assertTrue("To: liu1ee@uwindsor.ca" in msg.get_header())
        self.assertTrue("Date: {}".format(datetime.now().strftime("%Y-%m-%d")) in msg.get_header())

class MessageBodyTest(unittest.TestCase):

    def test_length(self):
        self.assertEqual(message.MessageBody("123").length(), 3)

    def test_string(self):
        self.assertEqual(message.MessageBody("123").__str__(), "123")

class TextMessageTest(unittest.TestCase):
    def setUp(self):
        self.tmsg = message.TextMessage("hello")

    def test_length(self):
        msg = self.tmsg
        self.assertTrue(str(message.CONTENTLENGTH + ": 5") in msg.get_header())
        self.assertTrue(str(message.CONTENTTYPE + ": text/plain") in msg.get_header())


if __name__ == '__main__':
    unittest.main()
