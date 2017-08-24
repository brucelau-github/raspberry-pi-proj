from appview import AppView
from Tkinter import *
from PIL import ImageTk
from PIL import Image as PILImage
import unittest

class AppViewTest(AppView):
    def __init__(self):
        AppView.__init__(self)
        #self.loadimage()
    def loadimage(self):
        img = PILImage.open('test-image.jpg')
        self.photo = ImageTk.PhotoImage(img)
        self.label.config(image = self.photo)

class ViewTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_showwindow(self):
        #app = AppView()
        app = AppViewTest()
        app.mainloop()

if __name__ == '__main__':
    unittest.main()
