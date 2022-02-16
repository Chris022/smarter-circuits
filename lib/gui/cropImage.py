import re
from tkinter import *
import cv2

from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk

class CropImage():

    def __init__(self, root, original_image):

        self.width = len(original_image[0])
        self.height = len(original_image)

        self.crop_start = (0,0)
        self.crop_end = (self.width, self.height)
        self.rects = []

        self.pressed = None

        self.canvas = Canvas(root, width=self.width, height=self.height)


        self.original_image = original_image
        self.convert_image(self.original_image)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor='nw', image=self.tkImg)

        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<Button>', self.button_pressed)
        self.canvas.bind('<ButtonRelease>', self.button_released)

    def convert_image(self, img):
        pilImg = PIL_Image.fromarray(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))
        self.tkImg = PIL_ImageTk.PhotoImage(image=pilImg)

    def convert_coord(self):
        x_left = self.crop_start[0] if self.crop_start[0] < self.crop_end[0] else self.crop_end[0]
        x_right = self.crop_start[0] if self.crop_start[0] > self.crop_end[0] else self.crop_end[0]
        y_top = self.crop_start[1] if self.crop_start[1] < self.crop_end[1] else self.crop_end[1]
        y_bot = self.crop_start[1] if self.crop_start[1] > self.crop_end[1] else self.crop_end[1]

        return [(x_left, y_top), (x_right, y_bot)]

    def draw_crop(self):
        for rect in self.rects:
            self.canvas.delete(rect)

        self.rects.append(self.canvas.create_rectangle(self.crop_start[0], self.crop_start[1], self.crop_end[0], self.crop_end[1], fill=''))

        [(x_left, y_top), (x_right, y_bot)] = self.convert_coord()

        self.rects.append(self.canvas.create_rectangle(0,0,self.width,y_top, fill='gray',stipple='gray50',outline=''))
        self.rects.append(self.canvas.create_rectangle(0,y_bot,self.width,self.height, fill='gray',stipple='gray50',outline=''))
        self.rects.append(self.canvas.create_rectangle(0,0,x_left,self.height, fill='gray',stipple='gray50',outline=''))
        self.rects.append(self.canvas.create_rectangle(x_right,0,self.width,self.height, fill='gray',stipple='gray50',outline=''))
    
    def get_rect(self):
        return self.convert_coord()

    def add(self):
         self.canvas.grid(row=0, column=0, rowspan=3)

    def remove(self):
         self.canvas.grid_remove()

    def motion(self, event):
        #print(event)
        if self.pressed:
            self.crop_end = (event.x, event.y)
            self.draw_crop()
        pass

    def button_pressed(self, event):
        #print(event)
        self.crop_start = (event.x, event.y)
        self.pressed = True
        pass

    def button_released(self, event):
        #print(event)
        self.pressed = False
        self.crop_end = (event.x, event.y)
        self.draw_crop()
        pass