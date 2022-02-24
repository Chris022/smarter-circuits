from lib.gui.guiUtils import *

from tkinter import *
import cv2



class CropImage():

    def __init__(self, root, position):

        self.position = position

        self.canvas = Canvas(root)

        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<Button>', self.button_pressed)
        self.canvas.bind('<ButtonRelease>', self.button_released)


    def convert_coord(self):
        x_left = self.crop_start[0] if self.crop_start[0] < self.crop_end[0] else self.crop_end[0]
        x_right = self.crop_start[0] if self.crop_start[0] > self.crop_end[0] else self.crop_end[0]
        y_top = self.crop_start[1] if self.crop_start[1] < self.crop_end[1] else self.crop_end[1]
        y_bot = self.crop_start[1] if self.crop_start[1] > self.crop_end[1] else self.crop_end[1]

        return [((int)(x_left), (int)(y_top)), ((int)(x_right), (int)(y_bot))]

    def draw_crop(self):

        if self.crop_start[0] < 0:
            self.crop_start = (0, self.crop_start[1])
        if self.crop_start[1] < 0:
            self.crop_start = (self.crop_start[0], 0)
        if self.crop_end[0] < 0:
            self.crop_end = (0, self.crop_end[1])
        if self.crop_end[1] < 0:
            self.crop_end = (self.crop_end[0], 0)

        if self.crop_start[0] > self.tkImg.width():
            self.crop_start = (self.tkImg.width(), self.crop_start[1])
        if self.crop_start[1] > self.tkImg.height():
            self.crop_start = (self.crop_start[0], self.tkImg.height())
        if self.crop_end[0] > self.tkImg.width():
            self.crop_end = (self.tkImg.width(), self.crop_end[1])
        if self.crop_end[1] > self.tkImg.height():
            self.crop_end = (self.crop_end[0], self.tkImg.height())

        for rect in self.rects:
            self.canvas.delete(rect)

        x_off, y_off = self.image_offset

        self.rects.append(self.canvas.create_rectangle(self.crop_start[0]+x_off, self.crop_start[1]+y_off, self.crop_end[0]+x_off, self.crop_end[1]+y_off, fill=''))

        [(x_left, y_top), (x_right, y_bot)] = self.convert_coord()

        self.rects.append(self.canvas.create_rectangle(0+x_off, 0+y_off, self.tkImg.width()+x_off, y_top+y_off, fill='gray',stipple='gray50',outline=''))
        self.rects.append(self.canvas.create_rectangle(0+x_off, y_bot+1+y_off, self.tkImg.width()+x_off, self.tkImg.height()+y_off, fill='gray',stipple='gray50',outline=''))
        self.rects.append(self.canvas.create_rectangle(0+x_off, 0+y_off, x_left+x_off, self.tkImg.height()+y_off, fill='gray',stipple='gray50',outline=''))
        self.rects.append(self.canvas.create_rectangle(x_right+1+x_off, 0+y_off, self.tkImg.width()+x_off, self.tkImg.height()+y_off, fill='gray',stipple='gray50',outline=''))
        
        self.canvas.update()

    def add(self, original_image):

        self.rects = []

        self.pressed = None
        self.cropped = False

        self.image_offset = (0,0)

        self.original_image = original_image

        self.image_width = len(original_image[0])
        self.image_height = len(original_image)

        self.crop_start = (1,2)

        self.canvas.configure(bg='#8f8f8f')
        self.tkImg = convert_to_tkImg(self.original_image)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=CENTER, image=self.tkImg)
        
        self.canvas.place(relx=self.position[0], rely=self.position[1], relwidth=self.position[2], relheight=self.position[3])
        
        self.canvas.update()
        self.resize()

        #self.canvas.coords(self.image_on_canvas, (int)(self.canvas.winfo_width()/2), (int)(self.canvas.winfo_height()/2))


    def resize(self):

        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.canvas.coords(self.image_on_canvas, (int)(self.canvas_width/2), (int)(self.canvas_height/2))

        factor = 1

        if self.image_width > self.image_height:
            factor = self.canvas_width/self.tkImg.width()
            k = self.image_height * (self.canvas_width/self.image_width)
            resized_image = cv2.resize(self.original_image, ((int)(self.canvas_width),(int)(k)), interpolation=cv2.INTER_AREA)
            self.tkImg = convert_to_tkImg(resized_image)
        else:
            factor = self.canvas_height/self.tkImg.height()
            k = self.image_width * (self.canvas_height/self.image_height)
            resized_image = cv2.resize(self.original_image, ((int)(k), (int)(self.canvas_height)), interpolation=cv2.INTER_AREA)
            self.tkImg = convert_to_tkImg(resized_image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.tkImg)

        self.factor = factor

        if self.cropped == False:
            self.crop_end = (self.tkImg.width(), self.tkImg.height()-1)
        else:
            self.crop_start = (factor*self.crop_start[0], factor*self.crop_start[1])
            self.crop_end = (factor*self.crop_end[0], factor*self.crop_end[1])

        self.image_offset = ((int)(self.canvas_width/2-self.tkImg.width()/2), (int)(self.canvas_height/2-self.tkImg.height()/2))
        self.draw_crop()


    def remove(self):
        self.canvas.place_forget()
        top, bot = self.convert_coord()

        for rect in self.rects:
            self.canvas.delete(rect)

        #print(self.factor)
        #print(self.original_image.shape)
        #print(top)
        #print(bot)
        top = ((int)(top[0]/self.factor), (int)(top[1]/self.factor))
        bot = ((int)(bot[0]/self.factor), (int)(bot[1]/self.factor))
        #print(top)
        #print(bot)

        crop_img = self.original_image[top[1]:bot[1], top[0]:bot[0]]

        #cv2.imwrite("test.png", crop_img)

        return crop_img


    def motion(self, event):
        #print(event)
        if self.pressed:
            self.crop_end = (event.x-self.image_offset[0], event.y-self.image_offset[1])
            self.draw_crop()
            #print(self.crop_end)
        pass

    def button_pressed(self, event):
        #print(event)
        self.cropped = True
        self.crop_start = (event.x-self.image_offset[0], event.y-self.image_offset[1])
        
        self.pressed = True
        pass

    def button_released(self, event):
        #print(event)
        self.pressed = False
        self.crop_end = (event.x-self.image_offset[0], event.y-self.image_offset[1])
        self.draw_crop()
        pass