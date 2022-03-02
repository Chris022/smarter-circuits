from tkinter import *
import cv2

from lib.gui.guiUtils import *


class CreateBinary():

    def __init__(self, root, position):

        self.position = position
        
        self.canvas = Canvas(root)

        self.reset = Button(root, text='Reset', command=self.reset_image)


        self.s1_value = IntVar()
        self.scale1 = Scale(root, from_=0, to=255, orient=HORIZONTAL, variable=self.s1_value, command=self.s1_changed)

        self.s2_value = IntVar()
        self.scale2 = Scale(root, from_=1, to=20, orient=HORIZONTAL, variable=self.s2_value, command=self.s2_changed)

        self.s3_value = IntVar()
        self.scale3 = Scale(root, from_=1, to=30, orient=HORIZONTAL, variable=self.s3_value, command=self.s3_changed)

        self.s4_value = IntVar()
        self.scale4 = Scale(root, from_=0, to=30, orient=HORIZONTAL, variable=self.s4_value, command=self.s4_changed)



    def s1_changed(self, event):
        (thresh, self.binary_image) = cv2.threshold(self.original_image, self.scale1.get(), 255, cv2.THRESH_BINARY)
        self.resize(self.binary_image)
    
    def s2_changed(self, event):
        img = cv2.medianBlur(self.original_image,self.scale2.get()*2+1)
        self.binary_image = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,self.scale3.get()*2+1,self.scale4.get())
        self.resize(self.binary_image)

    def s3_changed(self, event):
        img = cv2.medianBlur(self.original_image,self.scale2.get()*2+1)
        self.binary_image = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,self.scale3.get()*2+1,self.scale4.get())
        self.resize(self.binary_image)

    def s4_changed(self, event):
        img = cv2.medianBlur(self.original_image,self.scale2.get()*2+1)
        self.binary_image = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,self.scale3.get()*2+1,self.scale4.get())
        self.resize(self.binary_image)


    def add(self, image):
        self.original_image = image

        self.binary_image = (thresh, self.binary_image) = cv2.threshold(self.original_image, 127, 255, cv2.THRESH_BINARY)

        self.image_offset = (0,0)

        self.image_width = len(image[0])
        self.image_height = len(image)

        self.canvas.configure(bg='#8f8f8f')

        self.tkImg = convert_to_tkImg(self.original_image)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=CENTER, image=self.tkImg)
        

        self.canvas.place(relx=self.position[0], rely=self.position[1], relwidth=self.position[2], relheight=self.position[3])
        self.canvas.update()
        self.resize(self.original_image)

        self.reset.place(relx=0.8, rely=0.15, relwidth=0.1, relheight=0.05)


        self.scale1.place(relx=0.72, rely=0.3, relwidth=0.23, relheight=0.1)

        self.scale2.place(relx=0.72, rely=0.45, relwidth=0.23, relheight=0.1)
        self.scale3.place(relx=0.72, rely=0.55, relwidth=0.23, relheight=0.1)
        self.scale4.place(relx=0.72, rely=0.65, relwidth=0.23, relheight=0.1)

    def reset_image(self):
        self.resize(self.original_image)

    def resize(self, *arg):

        img = self.binary_image

        if len(arg) != 0:
            img = arg[0]


        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.canvas.coords(self.image_on_canvas, (int)(self.canvas_width/2), (int)(self.canvas_height/2))

        factor = 1

        if self.image_width > self.image_height:
            factor = self.canvas_width/self.tkImg.width()
            k = self.image_height * (self.canvas_width/self.image_width)
            resized_image = cv2.resize(img, ((int)(self.canvas_width),(int)(k)), interpolation=cv2.INTER_AREA)
            self.tkImg = convert_to_tkImg(resized_image)
        else:
            factor = self.canvas_height/self.tkImg.height()
            k = self.image_width * (self.canvas_height/self.image_height)
            resized_image = cv2.resize(img, ((int)(k), (int)(self.canvas_height)), interpolation=cv2.INTER_AREA)
            self.tkImg = convert_to_tkImg(resized_image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.tkImg)
    

    def remove(self):
        self.canvas.place_forget()

        self.reset.place_forget()

        self.scale1.place_forget()
        self.scale2.place_forget()
        self.scale3.place_forget()
        self.scale4.place_forget()
        
        return self.binary_image