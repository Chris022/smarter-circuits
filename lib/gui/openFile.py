
from tkinter import *
import cv2
from tkinter import filedialog as fd

from lib.gui.guiUtils import *

from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk

import numpy as np


class OpenFile():

    def __init__(self, root, next):

        self.image = np.zeros((100,100), dtype=np.uint8)

        #self.canvas_pos = position
        self.next = next

        self.open_button = Button(root, text='Open File', command=self.openFile)#width=10, height=2, command=self.openFile)
        #self.canvas = Canvas(root)

    def resize(self):
        return

    def openFile(self):
        path = fd.askopenfilename()
        
        self.image = cv2.imread(path)

        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        #self.image = resize(self.image, (650, None))

        resize = (650, None)

        width = len(self.image[0])
        height = len(self.image)

        if resize[0] != None and resize[1] == None:
            resize = (resize[0], (int)(height * resize[0] / width))
            self.image = cv2.resize(self.image, resize, interpolation = cv2.INTER_AREA)

        if resize[0] == None and resize[1] != None:
            resize = ((int)(width * resize[1] / height), resize[1])
            self.image = cv2.resize(self.image, resize, interpolation = cv2.INTER_AREA)

        if resize[0] != None and resize[1] != None:
            self.image = cv2.resize(self.image, resize, interpolation = cv2.INTER_AREA)

        self.next()


        #self.image = np.asarray(self.image)
        #
#
        #self.tkImg = convert_to_tkImg(self.image)
        #self.image_on_canvas = self.canvas.create_image(0, 0, anchor='nw', image=self.tkImg)

        #self.canvas.config(width=len(self.image[0]), height=len(self.image))
        #
        #self.canvas.place(relx=self.canvas_pos[0], rely=self.canvas_pos[1], relwidth=self.canvas_pos[2], relheight=self.canvas_pos[3])
        

    def add(self, *arg):
        #self.open_button.grid(row=4, column=0)
        self.open_button.place(relx=0.3, rely=0.7, relwidth=0.1, relheight=0.05)
         

    def remove(self):
        self.open_button.place_forget()
        #self.canvas.place_forget()

        return self.image