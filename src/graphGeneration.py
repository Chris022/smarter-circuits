from copy import deepcopy
import sys
sys.path.append('../')

import lib.utils as utils
#import classes
import matplotlib.pyplot as plt
import igraph as g
import json
import math as m
import cv2
import itertools
import igraph

import lib.graphLib.graph as g
from lib.graphLib.vertex import Vertex
from lib.graphLib.edge import Edge

import lib.graphProcessing as graphProcessing

from lib.utils import getPixel,colorPixels,isOneColor
from lib.constants import *
from lib.components.componentCollection import CLASS_OBJECTS


# Returns all Adjacent Pixels with a specific color
# image             -> 2D array with Pixel values
# pixel             -> coordinates of the pixel the others should be ajacent to
# color             -> the color of the "wanted" pixels
# blacklist         -> These pixels get ignored
def getAdjacentPixel(image,pixel,color,blacklist=[]):    
    adjacentPixels = [[-1,-1],[0,-1],[1,-1], \
                        [-1,0],        [1,0], \
                        [-1,1], [0,1], [1,1]]
    #create a array with the coordinates of all adjacentPixels
    validPixels = ([ pixel[0]+adj[0], pixel[1]+adj[1] ] for adj in adjacentPixels)
    #filter all pixels that are not the right color
    validPixels = list(
        filter(lambda coords: image[coords[1]][coords[0]] == color,validPixels)
    )
    #filter all pixels that are in the blacklist
    validPixels = list(
        filter(lambda x: not x in blacklist, validPixels)
    )

    return validPixels


# returns the coordinates of the first <color> pixel it finds
# returns -1 if no staring point is found
def findStaringPoint(image,color):
    for y in range(0,len(image)-1):
        for x in range(0,len(image[y])-1):
            if image[y][x] == color:
                return [x,y]
    return -1

class DirGradient:
    def __init__(self):
        self.queueX = []
        self.queueY = []

    def addStep(self,currentPosition,lastPosition):
        #get Direction
        xDir = 0
        yDir = 0

        if currentPosition[0] - lastPosition[0] > 0:
            xDir = 1
        elif currentPosition[0] - lastPosition[0] < 0:
            xDir = -1

        if currentPosition[1] - lastPosition[1] > 0:
            yDir = 1
        elif currentPosition[1] - lastPosition[1] < 0:
            yDir = -1

        self.queueX.append(xDir)
        self.queueY.append(yDir)
    
    def checkForEdge(self):
        #only gives a valid answer if there are more than 10 previous values
        if len(self.queueX) < 10: return False

        cSumX = sum(self.queueX[-5:]) # the latest 5 X coordinates
        cSumY = sum(self.queueY[-5:]) # the latest 5 Y coordinates
        length = m.sqrt(cSumX**2 + cSumY**2)
        currDir = (cSumX/length, cSumY/length)

        
        lSumX = sum(self.queueX[-10:-5]) # the 5 X coords 5 steps ago
        lSumY = sum(self.queueY[-10:-5]) # the 5 Y coords 5 steps ago
        length = m.sqrt(cSumX**2 + cSumY**2)
        lastDir = (lSumX/length, lSumY/length)

        dist = m.sqrt((currDir[0] - lastDir[0])**2 + (currDir[1] - lastDir[1])**2)

        if dist <= 0.8:
            return False

        return True

    def reset(self):
        self.queueX = []
        self.queueY = []



# Converts one connected Line into a Graph
#
# startPoint  -> coordinates of a Intersection
# color -> the color of the lines
# returns the generate graph and all visited Pixels
def generatePartGraph(image,startPoint,color):
    visitedPixels = []
    #graph = g.Graph(directed=False)
    #graph.add_vertex(str(startPoint), label=str(startPoint) ,color=INTERSECTION_COLOR)
    graph = g.Graph()

    #get white pixel adjacent!
    adjacentPixels = getAdjacentPixel(image,startPoint,color)
    if len(adjacentPixels) == 1:
        vertex = Vertex(color=END_COLOR, label=str(startPoint))
    elif len(adjacentPixels) == 2:
        vertex = Vertex(color=OTHER_NODE_COLOR, label=str(startPoint))
    else:
        vertex = Vertex(color=INTERSECTION_COLOR, label=str(startPoint))
    vertex.attr["coordinates"] = startPoint
    graph.addVertex(vertex)
    
    def recursiveGenerateGraph(currentPixel,lastPixel,lastGraphNode,oldDir):

        #create new copy of dir
        dir = deepcopy(oldDir)
        dir.addStep(currentPixel,lastPixel)

        #End Recursion if loop ends
        if currentPixel in visitedPixels:
            if len(graph.verticesWithLabel(str(currentPixel))):
                edge = Edge()
                v1 = graph.verticesWithLabel(str(lastGraphNode))[0]
                v2 = graph.verticesWithLabel(str(currentPixel))[0]
                graph.addEdge(edge,v1.id,v2.id)
            return

        visitedPixels.append(currentPixel)
        adjacentPixels = getAdjacentPixel(image,currentPixel,color,[lastPixel])
        if len(adjacentPixels) == 0:
            #ENDPOINT
            if(str(currentPixel) != lastGraphNode):
                #graph.add_vertex(str(currentPixel),label=str(currentPixel),color=END_COLOR)
                #graph.add_edge(str(lastGraphNode),str(currentPixel))
                vertex = Vertex(color=END_COLOR, label=str(currentPixel))
                vertex.attr["coordinates"] = currentPixel
                graph.addVertex(vertex)
                edge = Edge()
                v1 = graph.verticesWithLabel(str(lastGraphNode))[0]
                v2 = graph.verticesWithLabel(str(currentPixel))[0]
                graph.addEdge(edge,v1.id,v2.id)

        elif len(adjacentPixels) == 1:
            #LINE

            if dir.checkForEdge():
                vertex = Vertex(color=CORNER_COLOR, label=str(currentPixel))
                vertex.attr["coordinates"] = currentPixel
                graph.addVertex(vertex)
                edge = Edge()
                v1 = graph.verticesWithLabel(str(lastGraphNode))[0]
                v2 = graph.verticesWithLabel(str(currentPixel))[0]
                graph.addEdge(edge,v1.id,v2.id)
                dir.reset()
                recursiveGenerateGraph(adjacentPixels[0],currentPixel,str(currentPixel),dir)
            else:
                recursiveGenerateGraph(adjacentPixels[0],currentPixel,lastGraphNode,dir)
        else:
            #INTERSECTION
            if(str(currentPixel) != lastGraphNode):
                #graph.add_vertex(str(currentPixel),label=str(currentPixel),color=INTERSECTION_COLOR)
                #graph.add_edge(str(lastGraphNode),str(currentPixel))
                vertex = Vertex(color=INTERSECTION_COLOR, label=str(currentPixel))
                vertex.attr["coordinates"] = currentPixel
                graph.addVertex(vertex)
                edge = Edge()
                v1 = graph.verticesWithLabel(str(lastGraphNode))[0]
                v2 = graph.verticesWithLabel(str(currentPixel))[0]
                graph.addEdge(edge,v1.id,v2.id)
            dir.reset()
            for adjacentPixel in adjacentPixels:
                recursiveGenerateGraph(adjacentPixel,currentPixel,str(currentPixel),dir)

    recursiveGenerateGraph(startPoint,[0,0],str(startPoint),DirGradient())
    #befor returning, remove all "OTHER_NOTHE_COLOR" vertices
    clone = list(graph.ve.values())
    for vertex in clone:
        if vertex.color == OTHER_NODE_COLOR:
            graph.removeVertex(vertex.id)

    return graph,visitedPixels


def generateWholeGraph(image,foregroundColor,backgroundColor):
    graphCollection = []
    while True:
        startingPoint = findStaringPoint(image,foregroundColor)
        if startingPoint == -1:
            break
        if(startingPoint):
            G,visitedPixels = generatePartGraph(image,startingPoint,foregroundColor)
            graphCollection.append(G)
            #Remove all visited Pixels
            image = colorPixels(image,visitedPixels,backgroundColor)
        else:
            break
    return g.union(graphCollection)




# Takse a List of coordinates returns the coordinates of the upper left and lower right corner
def generateBoundingBox(verticesList,offset):

    listOfCoords = list(map(lambda x: x.attr['coordinates'],verticesList))

    xCoords = list(map(lambda x: x[0],listOfCoords))
    yCoords = list(map(lambda y: y[1],listOfCoords))

    #get smalles and biggest of each and create Box
    from_ = [min(xCoords)-offset,min(yCoords)-offset]
    to_ = [max(xCoords)+offset,max(yCoords)+offset]
    return [from_,to_]

def generateGraph(image):
     # Generate the Graph without the Cap connections
    union = generateWholeGraph(image,FOREGROUND,BACKGROUND)
    #call post Pattern Mathching
    for classses in CLASS_OBJECTS.values():
        union = classses.graphModification(union)
    #combine close tougether vertices
    allVertices = list(union.ve.values())
    intersectionVertices = list(filter(lambda x: x.color == INTERSECTION_COLOR,allVertices))
    union = graphProcessing.combineCloseVertices(union,intersectionVertices,INTERSECTION_COMBINATION_DIST)
    
    return union

#returns array of Tuples
#   Tuble (boundingBoxCoordinates, matchingVertices)
def getComponents(graph):
    patterns = list(map(lambda comp:comp.graphPattern(),CLASS_OBJECTS.values()))

    #remove double patterins
    components = []
    for comp in CLASS_OBJECTS.values():
        isIn = False
        for fp in components:
            if len(comp.graphPattern().getPatternMatches(fp.graphPattern())) > 0:
                isIn = True
        if not isIn:
            components.append(comp)

    matches = []
    for comp in components:
        newGraph = deepcopy(graph)
        newGraph = comp.prePatternMatching(newGraph)
        matchingInCopy = newGraph.getPatternMatches(comp.graphPattern())

        for i in matchingInCopy:
            a = []
            for j in i:
                a.append(graph.getVertex(j.id))
            matches.append(a)

    #matches = sum(matchingVertices,[])
    boundingBoxes = list(map(lambda x: generateBoundingBox(x,7),matches))
    components = zip(boundingBoxes,matches)
    return list(components)

#imageArray = load1Pixel("./../resources/img","preprocessed.png",binary=True)
#colorImage = load1Pixel("./../resources/img","preprocessed.png",color=True)

#boundingBoxes = generateBoudingBoxes(imageArray)
#print(len(boundingBoxes))
#for boundingBox in boundingBoxes:
#    drawRect(colorImage,boundingBox,(255,0,0))
#colorImage = cv2.cvtColor(255-colorImage, cv2.COLOR_BGR2RGB)
#plt.imshow(colorImage,interpolation="bilinear")
#plt.waitforbuttonpress(0)
