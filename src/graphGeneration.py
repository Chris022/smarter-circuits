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
import lib.graphLib.subisomorphismAlgorithm as algorithm

import lib.graphProcessing as graphProcessing

from lib.utils import getPixel,colorPixels,isOneColor
from lib.constants import *


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
        filter(lambda coords: getPixel(image,coords) == color,validPixels)
    )
    #filter all pixels that are in the blacklist
    validPixels = list(
        filter(lambda x: not x in blacklist, validPixels)
    )

    return validPixels

# returns the coordinates of the first <color> pixel it finds
def findStaringPoint(image,color):
    for y in range(0,len(image)):
        for x in range(0,len(image[y])):
            if getPixel(image,x,y) == color:
                return [x,y]

# Runs along line until it finds the first Intersection
#
# image      -> The image
# startPoint -> Any random Point on the line
# color      -> The color of the Line
def findFirstIntersection(image,startPoint,color):

    def recursiveFindValidPoint(currentPixel,lastPixel,dir):
        adjacentPixels = getAdjacentPixel(image,currentPixel,color)
        if len(adjacentPixels) > 2:
            return currentPixel
        elif len(adjacentPixels) == 1:
            return recursiveFindValidPoint(adjacentPixels[dir],currentPixel,-1)
        else:
            adjacentPixels = getAdjacentPixel(image,currentPixel,color,[lastPixel]) 
            return recursiveFindValidPoint(adjacentPixels[dir],currentPixel,dir)
    return recursiveFindValidPoint(startPoint,None,0)

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

    vertex = Vertex(color=INTERSECTION_COLOR, label=str(startPoint))
    vertex.attr["coordinates"] = startPoint
    graph.addVertex(vertex)
    
    def recursiveGenerateGraph(currentPixel,lastPixel,lastGraphNode,dirGradientOld):
        dirGradient = list(dirGradientOld)

        #get Direction
        if(abs(currentPixel[0] - lastPixel[0]) < abs(currentPixel[1] - lastPixel[1])):
            dirGradient.append(1)
        else:
            dirGradient.append(0)

        #End Recursion if loop ends
        if currentPixel in visitedPixels:
            #if len(graph.vs.select(name=str(currentPixel))):
            #    graph.add_edge(str(lastGraphNode),str(currentPixel))
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
            if len(dirGradient) > 6:
                currDire = sum(dirGradient[-4:])/4 < 0.5
                lastDire = sum(dirGradient[-5:-1])/4 < 0.5
                if not  currDire == lastDire:
                    #graph.add_vertex(str(currentPixel),label=str(currentPixel),color=CORNER_COLOR)
                    #graph.add_edge(str(lastGraphNode),str(currentPixel))
                    vertex = Vertex(color=CORNER_COLOR, label=str(currentPixel))
                    vertex.attr["coordinates"] = currentPixel
                    graph.addVertex(vertex)
                    edge = Edge()
                    v1 = graph.verticesWithLabel(str(lastGraphNode))[0]
                    v2 = graph.verticesWithLabel(str(currentPixel))[0]
                    graph.addEdge(edge,v1.id,v2.id)

                    recursiveGenerateGraph(adjacentPixels[0],currentPixel,str(currentPixel),dirGradient)
                else:
                    recursiveGenerateGraph(adjacentPixels[0],currentPixel,lastGraphNode,dirGradient)
            else:
                recursiveGenerateGraph(adjacentPixels[0],currentPixel,lastGraphNode,dirGradient)
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
            for adjacentPixel in adjacentPixels:
                recursiveGenerateGraph(adjacentPixel,currentPixel,str(currentPixel),[])

    recursiveGenerateGraph(startPoint,[0,0],str(startPoint),[])
    return graph,visitedPixels

def generateWholeGraph(image,foregroundColor,backgroundColor):
    graphCollection = []
    while True:
        startingPoint = findStaringPoint(image,foregroundColor)
        if(startingPoint):
            startingPoint = findFirstIntersection(image,startingPoint,foregroundColor)
            G,visitedPixels = generatePartGraph(image,startingPoint,foregroundColor)
            graphCollection.append(G)
            #Remove all visited Pixels
            image = colorPixels(image,visitedPixels,backgroundColor)
            if isOneColor(image,backgroundColor):
                print("end reached")
                break
        else:
            print("stoped before end")
            break
    return g.union(graphCollection)
    #return graphCollection

#Returns a List of all the Node Colors in a Graph
def getColorListNode(graph):
    colorList = []
    for vert in graph.ve:
        if vert.color == "red":
            colorList.append(0)
        elif vert.color == "blue":
            colorList.append(1)
        elif vert.color == "yellow":
            colorList.append(2)
        elif vert.color == "white":
            colorList.append(3)
    return colorList

#Returns a List of all the Edge Colors in a Graph
def getColorListEdge(graph):
    colorList = []
    for edge in graph.ed:
        try:
            if edge.color == "red":
                colorList.append(1)
            elif edge.color == "blue":
                colorList.append(2)
            elif edge.color == "yellow":
                colorList.append(3)
            elif edge.color == "white":
                colorList.append(4)
            elif edge.color == "green":
                colorList.append(5)
            else:
                colorList.append(0)
        except:
            colorList.append(0)
    return colorList

#Retuns a node by name
def getNode(graph,name):
    graph

def getPatternMatches(graph,pattern):
    mapings = algorithm.subisomorphism(graph, pattern)

    mapings = list(map(lambda match: set(match), mapings))

    
    #remove duplicated
    final = []
    for i in mapings:
        if i not in final:
            final.append(i)
    return list(map(lambda f: list(f), final))


# Takes a Graph
# Searches the Graph for Grounds
# checks if the "center" of a Ground is close to the "center" of another
# It then checks if there is more than one other Note between the two Intersections (To avoid the connection of 2 close tougheter Caps)
# if they are, the two Intersections are replaced with Other-Notes
# and they get connected by a Other Line
# returns: the modified Graph
def connectCapsTougehter(graph):
    groundGraph = groundPattern()

    # Match all ground Symbols
    groundMatches = getPatternMatches(graph,groundGraph)

    up = []
    down = []
    left = []
    right = []
    for groundMatchVertices in groundMatches:

        intersectionVertex = None
        for match in groundMatchVertices:
            if match.color == INTERSECTION_COLOR:
                intersectionVertex = match

        neighborVertices = graph.getNeighbors(intersectionVertex.id)

        for neighborVertex in neighborVertices:
            if not neighborVertex.color == 'blue':

                xOff = intersectionVertex.attr['coordinates'][0] - neighborVertex.attr['coordinates'][0]
                yOff = intersectionVertex.attr['coordinates'][1] - neighborVertex.attr['coordinates'][1]

                if abs(xOff) > abs(yOff):
                    if xOff > 0:
                        left.append(intersectionVertex)
                    else:
                        right.append(intersectionVertex)
                else:
                    if yOff > 0:
                        up.append(intersectionVertex)
                    else:
                        down.append(intersectionVertex)
                break

    for lCap in left:
        lCoord = lCap.attr['coordinates']

        rCoord = right[0].attr['coordinates']
        minDist = m.hypot(lCoord[0]-rCoord[0], lCoord[1]-rCoord[1])
        minCap = right[0]

        for rCap in right:
            rCoord = rCap.attr['coordinates']
            dist = m.hypot(lCoord[0]-rCoord[0], lCoord[1]-rCoord[1])

            if dist < minDist and graph.adjacent(lCap.id, rCap.id) == False:
                minDist = dist
                minCap = rCap

        lCap.color = OTHER_NODE_COLOR
        minCap.color = OTHER_NODE_COLOR
        graph.addEdge(Edge(color=OTHER_EDGE_COLOR),lCap.id, minCap.id)

    for dCap in down:
        dCoord = dCap.attr['coordinates']

        uCoord = up[0].attr['coordinates']
        minDist = m.hypot(dCoord[0]-uCoord[0], dCoord[1]-uCoord[1])
        minCap = up[0]

        for uCap in up:
            uCoord = uCap.attr['coordinates']
            dist = m.hypot(dCoord[0]-uCoord[0], dCoord[1]-uCoord[1])

            if dist < minDist and graph.adjacent(dCap.id, uCap.id) == False:
                minDist = dist
                minCap = uCap

        dCap.color = OTHER_NODE_COLOR
        minCap.color = OTHER_NODE_COLOR
        graph.addEdge(Edge(color=OTHER_EDGE_COLOR),dCap.id, minCap.id)

    return graph

# Ground Graph Patterns
def groundPattern():
    ground = g.Graph()
    v1 = Vertex(color=END_COLOR)
    v2 = Vertex(color=INTERSECTION_COLOR)
    v3 = Vertex(color=END_COLOR)
    ground.addVertex(v1)
    ground.addVertex(v2)
    ground.addVertex(v3)
    ground.addEdge(Edge(), v1.id, v2.id)
    ground.addEdge(Edge(), v3.id, v2.id)

    return ground


# Cap Graph Pattern
def capPattern():
    cap = g.Graph()
    v1 = Vertex(color=END_COLOR)
    v2 = Vertex(color=OTHER_NODE_COLOR)
    v3 = Vertex(color=END_COLOR)
    cap.addVertices([v1,v2,v3])
    cap.addEdge(Edge(), v1.id, v2.id)
    cap.addEdge(Edge(), v3.id, v2.id)

    v4 = Vertex(color=END_COLOR)
    v5 = Vertex(color=OTHER_NODE_COLOR)
    v6 = Vertex(color=END_COLOR)
    cap.addVertices([v4,v5,v6])
    cap.addEdge(Edge(), v4.id, v5.id)
    cap.addEdge(Edge(), v6.id, v5.id)

    cap.addEdge(Edge(color=OTHER_EDGE_COLOR), v2.id, v5.id)
    return cap

# Resistor Graph Pattern
def resistorPattern():
    res = g.Graph()
    v1 = Vertex(color=INTERSECTION_COLOR)
    v2 = Vertex(color=CORNER_COLOR)
    v3 = Vertex(color=CORNER_COLOR)
    v4 = Vertex(color=INTERSECTION_COLOR)
    v5 = Vertex(color=CORNER_COLOR)
    v6 = Vertex(color=CORNER_COLOR)
    res.addVertices([v1,v2,v3,v4,v5,v6])
    res.addEdge(Edge(), v1.id, v2.id)
    res.addEdge(Edge(), v2.id, v3.id)
    res.addEdge(Edge(), v3.id, v4.id)
    res.addEdge(Edge(), v4.id, v5.id)
    res.addEdge(Edge(), v5.id, v6.id)
    res.addEdge(Edge(), v6.id, v1.id)
    
    return res

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
    # Connect Caps
    union = connectCapsTougehter(union)
    #combine close tougether vertices
    allVertices = list(union.ve.values())

    #intersectionVertices
    intersectionVertices = list(filter(lambda x: x.color == INTERSECTION_COLOR,allVertices))

    union = graphProcessing.combineCloseVertices(union,intersectionVertices,INTERSECTION_COMBINATION_DIST)
    
    return union

#returns array of Tuples
#   Tuble (boundingBoxCoordinates, matchingVertices)
def getComponents(graph):
    patterns =  [    capPattern(), \
                resistorPattern(), \
                groundPattern(), \
            ]
    matchingVertices = (getPatternMatches(graph, pattern) for pattern in patterns)
    matches = sum(matchingVertices,[])
    boundingBoxes = list(map(lambda x: generateBoundingBox(x,7),matches))
    components = zip(boundingBoxes,matches)
    return list(components)

#imageArray = load1Pixel("./../src/testImages","2.png",binary=True)
#colorImage = load1Pixel("./../src/testImages","2.png",color=True)
#
#boundingBoxes = generateBoudingBoxes(imageArray)
#print(len(boundingBoxes))
#for boundingBox in boundingBoxes:
#    drawRect(colorImage,boundingBox,(255,0,0))
#colorImage = cv2.cvtColor(255-colorImage, cv2.COLOR_BGR2RGB)
#plt.imshow(colorImage,interpolation="bilinear")
#plt.waitforbuttonpress(0)
