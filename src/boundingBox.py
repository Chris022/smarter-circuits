from classes import point,Point,Rect,rect
import numpy
import math
from typing import List

#--------------------------helper functions-----------------------
def getDistance(point1,point2):
    return math.sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2)

def getClosestPoint(point,pointList):
    # remove the point form the point List
    pointList = list(filter(lambda p: p != point,pointList))
    distances = list(map(lambda p: getDistance(point,p),pointList))
    indexOfMinimum = numpy.argmin(distances)
    return pointList[indexOfMinimum]

def getNClosestPoint(point,pointList,n):
    # remove the point form the point List
    pointList = list(filter(lambda p: p != point,pointList))
    distances = numpy.array(list(map(lambda p: getDistance(point,p),pointList)))
    indexiesOfMinima = (distances).argsort()[:n]
    elements = list(map(lambda index: pointList[index],indexiesOfMinima))
    return elements

def getNearPoints(point,pointList,dist):
    # remove the point form the point List
    pointList = list(filter(lambda p: p != point,pointList))
    # get the distances from the point to each point of the point List
    distances = map(lambda p: getDistance(point,p),pointList)
    distances = numpy.array(list(distances))

    elements = []
    # add every point, that has a distance smaller than dist to the elements array
    for i in range(0,len(distances)):
        if distances[i] <= dist:
            elements.append(pointList[i])
    return elements

def getPointsThatAreInTheRect(points: List[point],box: rect) -> List[point]:
    pointsIn = []
    for point in points:
        if point.x >= box.center.x - box.radius and point.x <= box.center.x + box.radius:
            if point.y >= box.center.y - box.radius and point.y <= box.center.y + box.radius:
                pointsIn.append(point)
    return pointsIn

def algorithm1(intersectionList,endPointList):
    rectList = []
    rectOffset = 4
    for intersection in intersectionList:
        closestPoint = getClosestPoint(intersection,intersectionList)
        center = Point((closestPoint.x-intersection.x)/2+intersection.x,(closestPoint.y-intersection.y)/2+intersection.y)

        distToClosePoint = math.floor(getDistance(closestPoint,center))
        nerestEndPoints = getNearPoints(center,endPointList,distToClosePoint*3)

        if(len(nerestEndPoints) != 0):
            dist = max(  list(  map(lambda x: getDistance(x,center),nerestEndPoints)))
        else:
            dist = distToClosePoint
        
        boundingBox = Rect(center,dist+rectOffset)
        #improvement
        #check if there are exactily 0 or 4 endpoins in the rect
        endpointsInBoundingBox = len(getPointsThatAreInTheRect(endPointList,boundingBox))
        if endpointsInBoundingBox == 0 or endpointsInBoundingBox == 4:
            rectList.append(boundingBox)
    return rectList

def algorithm2(intersectionList,endPointList):
    rectList = []
    for intersection in intersectionList:
        closestPoints = getNClosestPoint(intersection,endPointList,n=2)
        dist = max(list(map(lambda x: getDistance(x,intersection),closestPoints)))
        boundingBox = Rect(intersection,dist)
        #improvement
        #check if there are any intersection points in the bounding box
        intersectionPointsInBoundinBox = len(getPointsThatAreInTheRect(intersectionList,boundingBox))
        if intersectionPointsInBoundinBox <= 1:
            rectList.append(boundingBox)
    return rectList


#main function
def getBoundingBox(intersectionList: List[point], endPointList: List[point]):
    # Algorithm 1
    rectList1 = algorithm1(intersectionList,endPointList)

    # Algorithm 2 
    rectList2 = algorithm2(intersectionList,endPointList)

    return rectList1 + rectList2