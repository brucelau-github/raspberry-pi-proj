import unittest
import re
import message
import StringIO
from PIL import Image, ImageTk
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


class TextMessageTest(unittest.TestCase):
    def setUp(self):
        self.tmsg = message.TextMessage()

    def test_length(self):
        msg = self.tmsg
        msg.set_text_body("hello")
        self.assertTrue(str(message.CONTENTLENGTH + ": 5") in msg.get_header())
        self.assertTrue(str(message.CONTENTTYPE + ": text/plain") in msg.get_header())

class ImageMessageTest(unittest.TestCase):
    def setUp(self):
        self.img = message.ImageMessage()
        self.img.load_from_filepath(filepath="test-image.jpg")


    def test_imageparser(self):
        img = self.img
        raw_data = img.as_string()
        parsedimg = message.ImageMessage()
        parsedimg.parse_fromstr(msgstring=raw_data)
        self.assertEqual(parsedimg._body, img._body)
        self.assertDictEqual(parsedimg._header, img._header)


if __name__ == '__main__':
    unittest.main()
