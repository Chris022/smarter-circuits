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
def loadImage(path, name, transpose=False, resize=(650, 450), invert=False, color=False, binary=False):
    image = cv2.imread('{path}/{name}'.format(path=path,name=name))
    image = cv2.resize(image, resize, interpolation = cv2.INTER_AREA)
    if not color:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        if binary:
            for y in range(0, len(image)):
                for x in range(0, len(image[y])):
                    if image[y][x] < 125:
                        image[y][x] = 0
                    else:
                        image[y][x] = 255
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return np.asarray(image)

def load1PixelBinary(path, name):
    image = cv2.imread('{path}/{name}'.format(path=path,name=name))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    for y in range(0, len(image)):
        for x in range(0, len(image[y])):
            if image[y][x] < 125:
                image[y][x] = 0
            else:
                image[y][x] = 255
                
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

# coords can either be a array with x y value or two seperate arguments with x and y
def getPixel(image,*coords):
    if len(coords) == 1:
        return image[coords[0][1]][coords[0][0]]
    else:
        return image[coords[1]][coords[0]]

# coords can either be a array with x y value or two seperate arguments with x and y
def setPixel(image,color,*coords):
    if len(coords) == 1:
        image[coords[0][1]][coords[0][0]] = color
        return image
    else:
        image[coords[1]][coords[0]] = color
        return image

# colors all the given pixels in an image
def colorPixels(image,pixels,color):
    for visitedPixel in pixels:
        image = setPixel(image,color,visitedPixel[0],visitedPixel[1])
    return image

# check if the whole image has only one Color
def isOneColor(image,color):
    for i in image:
        for j in i:
            if not j == color:
                return False
    return True

# Draws a Rectangle
def drawRect(image,boundingBoxes,color):
    corner1 = boundingBoxes[0]
    corner2 = boundingBoxes[1]
    startX = corner1[0]
    startY = corner1[1]

    endX = corner2[0]
    endY = corner2[1]

    for x in range(startX,endX):
        image[startY][x] = color
        image[endY][x] = color

    for y in range(startY,endY):
        image[y][startX] = color
        image[y][endX] = color

    return image