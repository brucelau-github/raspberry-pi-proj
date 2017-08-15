import threading
from Tkinter import *
from connector import AppConnector

class App:
    def __init__(self):
        self.root = Tk()
        self.full_screen()
        self.connector = AppConnector(app=self)

        self.msg = StringVar()
        self.msg.set("test")
        self.label = Label(self.root, textvariable=self.msg, fg="red")
        self.label.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.button = Button(self.root, text="quit", fg="red", command=self.root.quit)
        self.button.place(relx=0.3, rely=0.8, anchor=S)

        self.hi_there = Button(self.root, text="Hello", command=self.say_hi)
        self.hi_there.place(relx=0.7, rely=0.8, anchor=S)


    def say_hi(self):
        self.msg.set("hello world")

    def update_msg(self, msg=''):
        self.msg.set(msg)

    def run(self):
        self.connector_thread = threading.Thread(target=self.connector.serve_forever)
        self.connector_thread.start()
        self.root.mainloop()

    def close(self):
        self.connector.request_shutdown = True
        self.connector_thread.join()
        self.connector.disconnect()
        self.root.destroy()
    def full_screen(self):
        self.root.overrideredirect(False)
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))

