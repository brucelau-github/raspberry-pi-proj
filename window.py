from Tkinter import *

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.label = Label(frame, text="quit", fg="red")
        self.label.pack(side=TOP)

        self.button = Button(frame, text="quit", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print "hi there, everyone!"

root = Tk() #create basic window

app = App(root)
root.mainloop() #keep the windows showing
root.destroy()
