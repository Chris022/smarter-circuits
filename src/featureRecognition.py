import numpy
import math
import classes

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

def rotateFilters(filters):
    rotatedFilters = []
    for filter in filters:
        for k in range(0,4):
            rotatedFilters.append(numpy.rot90(filter, k))
    return rotatedFilters

def getFeatures(image):

    # filter white regions
    whiteFeatures = whiteFilter(image)
    points = []
    for y in range(1, len(whiteFeatures)-1):
        for x in range(1, len(whiteFeatures[y])-1):
            if whiteFeatures[y][x] == 0:
                points.append((x,y))

    # create filters
    filters = []
    filters.append([[0,0,0],[0,255,255],[0,0,0]])
    filters.append([[255,0,0],[0,255,0],[0,0,0]])
    endPointFilters = rotateFilters(filters)

    # apply endpoint filters
    endPoints = []
    for filter in endPointFilters:
        endPoints = endPoints + applyFilter(filter, image, points)


    filters = []
    filters.append([[0,0,0],[255,255,255],[0,255,0]])
    filters.append([[0,0,0],[255,0,255],[0,255,0]])
    filters.append([[255,0,0],[0,255,255],[0,255,0]])
    filters.append([[0,0,255],[255,255,255],[0,255,0]])
    filters.append([[255,0,0],[255,255,255],[0,255,0]])
    filters.append([[0,255,0],[0,255,255],[255,255,255]])
    filters.append([[255,0,255],[0,255,255],[0,255,0]])
    filters.append([[255,0,255],[255,255,0],[0,255,0]])
    intersectionFilters = rotateFilters(filters)

    # apply intersection filters
    intersections = []
    for filter in intersectionFilters:
        intersections = intersections + applyFilter(filter, image, points)

    # remove unnecessary intersections
    filteredIntersections = []

    filteredIntersections.append(intersections[0])
    intersections.remove(intersections[0])

    for inter in intersections:
        connected = False
        for filtered in filteredIntersections:
            dist = math.sqrt((inter[0] - filtered[0])**2 + (inter[1] - filtered[1])**2)
            if dist < 2:
                connected = True
        if not connected:
            filteredIntersections.append(inter)

    endPointsAsPoints = list(map(lambda x: classes.Point(x[1], x[0]), endPoints))
    intersectionsAsPoints = list(map(lambda x: classes.Point(x[1], x[0]), filteredIntersections))

    return endPointsAsPoints, intersectionsAsPoints

