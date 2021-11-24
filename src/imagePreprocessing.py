import numpy as np
import cv2
import utils

def getRegion(pos, image):
    return np.transpose(image[pos[0]-1:pos[0]+2, pos[1]-1:pos[1]+2])

def equal(filter, img):
    for x in range(0, len(filter)):
        for y in range(0, len(filter[0])):
            if filter[x][y] != -1 and filter[x][y] != img[x][y]:
                return False
    return True

def applyFilterOnPoints(filter, image, points):
    features = []
    for (x, y) in points:
        try:
            if equal(filter, getRegion((x, y), image)):
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
            flipped += [np.flip(features[i][0],1), np.flip(features[i][1],1)]
            pass 
        features += flipped
    return features

def getFeatures():
    features = []

    feature = [[0,255,0],[255,255,255],[0,255,0]]
    replacement = [[255,0,0],[0,0,0],[255,0,255]]
    features += addFeature(feature, replacement, rotate=False)

    feature = [[0,255,-1],[-1,255,255],[255,255,-1]]
    replacement = [[0,255,255],[-1,255,0],[255,255,-1]]
    features += addFeature(feature, replacement, flip=True)

    feature = [[-1,0,255],[255,255,0],[0,255,-1]]
    replacement = [[-1,0,255],[255,0,255],[0,255,-1]]
    features += addFeature(feature, replacement)

    feature = [[-1,0,-1],[255,255,255],[0,255,0]]
    replacement = [[-1,0,-1],[255,0,255],[0,255,0]]
    features += addFeature(feature, replacement)

    feature = [[-1,0,0],[255,255,0],[0,255,-1]]
    replacement = [[-1,0,0],[255,0,0],[0,255,-1]]
    features += addFeature(feature, replacement)

    return features

def preprocessImage(image):

    (thresh, binary) = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)

    points = []
    for x in range(0, len(binary)):
        for y in range(0, len(binary[x])):
            if binary[x][y] == 255:
                points.append((x,y))

    filter = np.full((13, 13), 255)
    features = applyFilterOnPoints(filter, binary, points)

    for (x,y) in features:
        binary[x][y] = 0

    thinn = utils.thinnImage(binary)

    features = getFeatures()

    for feature in features:
        featureList = applyFilterOnPoints(feature[0], thinn, points)
        for (xOff, yOff) in featureList:
            for y in range(0, len(feature[1])):
                for x in range(0, len(feature[1][y])):
                    if feature[1][y][x] != -1:
                        thinn[xOff + x - 1][yOff + y - 1] = feature[1][y][x]

    return thinn
