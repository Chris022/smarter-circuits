import cv2
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk

def convert_to_tkImg(img):
        pilImg = PIL_Image.fromarray(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))
        tkImg = PIL_ImageTk.PhotoImage(image=pilImg)
        return tkImg

#def resize(image, resize):
#    width = len(image[0])
#    height = len(image)
#    if resize[0] != None and resize[1] == None:
#        resize = (resize[0], (int)(height * resize[0] / width))
#        image = cv2.resize(image, resize, interpolation = cv2.INTER_AREA)
#    if resize[0] == None and resize[1] != None:
#        resize = ((int)(width * resize[1] / height), resize[1])
#        image = cv2.resize(image, resize, interpolation = cv2.INTER_AREA)
#    if resize[0] != None and resize[1] != None:
#        image = cv2.resize(image, resize, interpolation = cv2.INTER_AREA)
#    return image