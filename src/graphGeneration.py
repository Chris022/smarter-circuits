from copy import deepcopy
import igraph as g

import sys
from lib.components.componentCollection import PATTERNS
sys.path.append('../')


from lib.utils import colorPixels,getAdjacentPixel
from lib.dirGradient import DirGradient

from lib.constants import *


import lib.graphLib.graph as g
from lib.graphLib.vertex import Vertex
from lib.graphLib.edge import Edge

import lib.graphProcessing as graphProcessing


# returns the coordinates of the first <color> pixel it finds
# returns -1 if no staring point is found
def findStaringPoint(image,color):
    for y in range(0,len(image)-1):
        for x in range(0,len(image[y])-1):
            if image[y][x] == color:
                return [x,y]
    return -1

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

def generateGraph(image):
    copyImage = deepcopy(image)

    # Generate the Graph
    graphList = []
    while True:
        startingPoint = findStaringPoint(copyImage,FOREGROUND)
        if startingPoint == -1:
            break
        subGraph,visitedPixels = generatePartGraph(copyImage,startingPoint,FOREGROUND)
        graphList.append(subGraph)
        #Remove all visited Pixels
        copyImage = colorPixels(copyImage,visitedPixels,BACKGROUND)
    graph = g.union(graphList)

    #combine close together vertices
    allVertices = list(graph.ve.values())
    intersectionVertices = list(filter(lambda x: x.color == INTERSECTION_COLOR,allVertices))
    graph = graphProcessing.combineCloseVertices(graph,intersectionVertices,INTERSECTION_COMBINATION_DIST)
    return graph