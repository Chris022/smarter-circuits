import cv2
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk

def convert_to_tkImg(img):
        pilImg = PIL_Image.fromarray(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))
        tkImg = PIL_ImageTk.PhotoImage(image=pilImg)
        return tkImg