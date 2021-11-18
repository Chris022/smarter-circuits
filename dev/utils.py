import numpy as np
import cv2

#create an independent copy of a numpy array
def createIndependetCopy(img):
    newImg = np.empty_like(img)
    newImg[:] = img
    return newImg

def zip2d(arg0, arg1, arg2):
    arr = np.zeros((len(arg0),len(arg0[0]),3))
    for x in range(0, len(arr)):
        for y in range(0, len(arr[x])):
            arr[x][y] = (arg0[x][y], arg1[x][y], arg2[x][y])
    return arr

# load image
def loadImage(path, name, transpose = True, resize = (650, 450), invert = True, color = False):
    image = cv2.imread('{path}/{name}'.format(path=path,name=name))
    if not color:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.resize(image, resize, interpolation = cv2.INTER_AREA)
    if invert:
        image = 255 - image
    if transpose:
        image = np.transpose(image)
    return np.asarray(image)

def thinnImage(image):
    image = cv2.ximgproc.thinning(image)
    return image

def saveImage(name, image, invert = True, color=False):
    image = np.transpose(image)
    if not color:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    if invert:
        cv2.imwrite('./img/' + name, 255 - image)
    else:
        cv2.imwrite('./img/' + name, image)

# Runs the function on every Pixel in the image
def foreachPixel(image,function):
    for y in range(0,len(image)):
        for x in range(0,len(image[y])):
            function(image[y][x])

# apply a function to every pixel
def mapPixel(image,function):
    newImage = createIndependetCopy(image)
    for y in range(0,len(image)):
        for x in range(0,len(image[y])):
            newImage[y][x] = function(image[y][x])
    return newImage