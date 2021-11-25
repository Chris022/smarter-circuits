import numpy as np
import cv2
import utils
import math

def getRegion(size, pos, image):
    xOff = math.floor(size[0]/2)
    yOff = math.floor(size[1]/2)
    return image[pos[1]-yOff:pos[1]+yOff+1, pos[0]-xOff:pos[0]+xOff+1]

def equal(filter, img):
    for y in range(0, len(filter)):
        for x in range(0, len(filter[y])):
            if filter[y][x] != -1 and filter[y][x] != img[y][x]:
                return False
    return True

def applyFilterOnPoints(filter, image, points):
    features = []
    size = [len(filter), len(filter[0])]
    for (x, y) in points:
        try:
            if equal(filter, getRegion(size, (x, y), image)):
                features.append((x,y))
        except:
            pass
    return features

def rotateFilter(filter):
    rotatedFilters = []
    for k in range(0,4):
        rotatedFilters.append(np.rot90(filter, k))
    return rotatedFilters

def addFeature(feature, replacement, rotate=True, flip=False):
    features = []
    if rotate:
        feature = rotateFilter(feature)
        replacement = rotateFilter(replacement)
        for i in range(0,4):
            features.append([feature[i], replacement[i]])
    else:
        features.append([feature, replacement])
    if flip:
        flipped = []
        for i in range(0, len(features)):
            flipped.append([np.flip(features[i][0],1), np.flip(features[i][1],1)])
        features += flipped
    return features

def getFeatures():
    features = []
    
    feature = [[255,0,255],[0,0,0],[255,0,255]]
    replacement = [[0,255,255],[255,255,255],[0,255,0]]
    features += addFeature(feature, replacement, rotate=False)

    feature = [[255,0,-1],[-1,0,0],[0,0,-1]]
    replacement = [[255,0,0],[-1,0,255],[0,0,-1]]
    features += addFeature(feature, replacement, flip=True)

    feature = [[-1,255,0],[0,0,255],[255,0,-1]]
    replacement = [[-1,255,0],[0,255,0],[255,0,-1]]
    features += addFeature(feature, replacement)
    
    feature = [[-1,255,-1],[0,0,0],[255,0,255]]
    replacement = [[-1,255,-1],[0,255,0],[255,0,255]]
    features += addFeature(feature, replacement)
    
    feature = [[-1,255,255],[0,0,255],[255,0,-1]]
    replacement = [[-1,255,255],[0,255,255],[255,0,-1]]
    features += addFeature(feature, replacement)

    return features

def preprocessImage(image):

    (thresh, binary) = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)

    points = []
    for y in range(0, len(binary)):
        for x in range(0, len(binary[y])):
            if binary[y][x] == 0:
                points.append((x,y))

    filter = np.full((13, 13), 0)
    features = applyFilterOnPoints(filter, binary, points)

    for (x,y) in features:
        binary[y][x] = 255

    thinn = utils.thinnImage(binary)

    features = getFeatures()

    for feature in features:
        featureList = applyFilterOnPoints(feature[0], thinn, points)
        for (xOff, yOff) in featureList:
            for y in range(0, len(feature[1])):
                for x in range(0, len(feature[1][y])):
                    if feature[1][y][x] != -1:
                        thinn[yOff + y - 1][xOff + x - 1] = feature[1][y][x]

    return thinn
