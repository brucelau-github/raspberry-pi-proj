import datetime
import re
import PIL
import StringIO

"""protocol defined here
Headers
"""
FROM = "From"
TO = "To"
DATE = "Date"
CONTENTTYPE = "Content-type"
CONTENTLENGTH = "Content-length"

class Message:
    """Basic message object inheritated by TextMessage, ImageMessage, AudioMessage
    create some common method to overwrite by subclass
    """
    def __init__(self):
        """constructor method
        generate default current time as Date
        """
        self.set_default_header()
        self._body = None

    def __str__(self):
        pass

    def set_default_header(self):
        self.set_header(DATE, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.set_header(FROM, "Message Center Server")

    def get_header(self):
        if not self._header:
            return None
        ret_str = ""
        for k, v in self._header.items():
            ret_str = ret_str + '{0}: {1}\n'.format(str(k),str(v))
        return ret_str

    def get_header_as_string(self):
        return self.get_header()

    def set_header(self, key, value):
        if not hasattr(self, '_header'):
            self._header = {}
        self._header[key] = value

    def set_body(self, body=None):
        self._body = body
        self.set_header(CONTENTLENGTH,str(len(body)))


    def as_string(self):
        return self.get_header_as_string() + "\n" + self._body

    def parse_fromstr(self, msgstring):
        parsr = MessageParser(messagestring=msgstring)
        self._body = parsr.get_payload()
        self._header = parsr.get_header()

    def parse_fromobj(self, msgobj):
        self._header = msgobj._header
        self._body = msgobj._body

    def is_image(self):
        return self._header[CONTENTTYPE] == ImageMessage.IMAGE

    def get_body_length(self):
        return int(self._header[CONTENTLENGTH])

    def append_body(self, data):
        self._body +=data


class TextMessage(Message):
    """a simple text message class
    wrap only a text message
    """
    TEXT = 'text/plain'
    def __init__(self):
        Message.__init__(self)
        self.set_header(CONTENTTYPE, self.TEXT)

    def set_text_body(self, text=""):
        self.set_body(text)

    def get_body(self):
        return self._body


class ImageMessage(Message):
    """a image message wrapper
    to wrap a single image message
    """
    IMAGE="image/jpg"
    def __init__(self):
        Message.__init__(self)
        self.set_header(CONTENTTYPE, self.IMAGE)

    def load_from_filepath(self, filepath=""):
        if not filepath:
            return None
        try:
            with open(filepath) as f:
                data = f.read()
        except IOError:
            data = None
            print("file not exist")
            f.colse()
            return None
        self.set_body(data)

    def get_image(self):
        imgfile = PIL.Image.open(StringIO.StringIO(self._body))
        return imgfile


class MessageParser:
    def __init__(self, messagestring=''):
        self.header_string = ""
        self.headers = None
        self.payload = None
        self.messagestring = messagestring
        self._parse(messagestring)

    def _parse(self, messagestring=''):
        data_list = re.split(r'\n\n', messagestring, 1)
        if len(data_list) != 2:
            self.header = None
            self.playload = None
            return None
        self.header_string, self.payload = data_list[0], data_list[1]

    def get_payload(self):
        return self.payload

    def get_header(self):
        _headers = {}
        hd_list = self.header_string.split('\n')
        for hdr in hd_list:
            k, v = re.split(r': ', hdr, 1)
            _headers[k] = v
        self.headers = _headers
        return self.headers
