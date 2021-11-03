import numpy
import math

def getRegion(filter, x, y, image):
    yOffset = math.floor(len(filter)/2)
    xOffset = math.floor(len(filter[0])/2)
    return image[y-yOffset:y+yOffset+1, x-xOffset:x+xOffset+1]

def whiteFilter(image):
    filter = numpy.asarray([[0,0,0],[0,0,0],[0,0,0]])
    image = numpy.asarray(image)
    features = numpy.empty_like(image)
    for y in range(1,len(image)-1):
        for x in range(1,len(image[y])-1):
            if numpy.all(numpy.equal(filter, getRegion(filter, x, y, image))):
                features[y][x] = 255
            else:
                features[y][x] = 0
    return features

def applyFilter(filter, image, points):
    image = numpy.asarray(image)
    features = []
    for (x, y) in points:
        if numpy.all(numpy.equal(filter, getRegion(filter, x, y, image))):
            features.append((x,y))
    return features