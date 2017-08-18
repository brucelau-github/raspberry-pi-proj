import datetime

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
        self.set_header(DATE, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def __str__(self):
        pass

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

    def set_body(self, messagebody=None):
        self.messagebody = messagebody
        self.set_header(CONTENTLENGTH,messagebody.length())

    def get_body_as_string(self):
        if not self.messagebody:
            return ""
        return self.messagebody.as_string()

    def as_string(self):
        return self.get_header_as_string() + "\n" + self.get_body_as_string()


class MessageBody:
    def __init__(self, body=None):
        self.body = body

    def length(self):
        return len(self.body)

    def __str__(self):
        return self.as_string()

    def as_string(self):
        return self.body

class TextMessage(Message):
    """a simple text message class
    wrap only a text message
    """
    def __init__(self, text_message=None):
        Message.__init__(self)
        self.set_body(MessageBody(text_message))
        self.set_header(CONTENTTYPE, 'text/plain')
