from Tkinter import *

class App:
    def __init__(self):
        self.root = Tk()
        frame = Frame(self.root)
        frame.pack()

        self.msg = StringVar()
        self.msg.set("test")
        self.label = Label(frame, textvariable=self.msg, fg="red")
        self.label.pack(side=TOP)

        self.button = Button(frame, text="quit", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        self.msg.set("hello world")

    def updatemsg(self, msg=''):
        self.msg.set(msg)

    def run(self):
        self.root.mainloop()

    def close(self):
        self.root.destroy()

