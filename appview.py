from PIL import ImageTk
from connector import AppConnector
from message import ImageMessage
from PIL import Image as PILImage
from Tkinter import *
import threading

class AppView(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.init_connector()
        self.title('Raspberry Pi Client')
        self.label = Label(self)
        self.full_screen()
        self.label.place(relx=0.5, rely=0.5, anchor=CENTER)

    def init_connector(self):
        self.connector = AppConnector(app=self)

    def update_msg(self, msg=None):
        if not msg:
            return
        self.label.config(text=msg.get_body(), image=None)

    def update_image(self, msg=None):
        if not msg:
            return
        self.photo = ImageTk.PhotoImage(msg.get_image())
        self.label.config(image=self.photo)

    def mainloop(self):
        self.connector.thread_serve_forever()
        Tk.mainloop(self)

    def pack(self):
        self.label.pack(fill=BOTH)

    def destroy(self):
        Tk.destroy(self)
        self.connector.shutdown()

    def full_screen(self):
        self.overrideredirect(False)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
