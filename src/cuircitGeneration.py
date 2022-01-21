import sys
sys.path.append('../')

import lib.graphLib.graph as g
from lib.graphLib.vertex import Vertex
from lib.graphLib.edge import Edge

from lib.constants import *
from lib.utils import convertToIgraph

import igraph
import copy
import math

def recolorCap(graph):
    for vertex in graph.ve.values():
        if vertex.color == OTHER_NODE_COLOR:
            vertex.color = INTERSECTION_COLOR
    return graph

def toRelative(buildingPartDefinitons,graph):
    #get lenght of the longest resistor
    len = -1
    for buildingPart in buildingPartDefinitons:
        vertices = buildingPart[2]
        rotation = buildingPart[1]
        type_ = buildingPart[0]

        if not type_ == CLASS_OBJECT_NAMES["res"]:
            continue
        
        xVals = list(map(lambda v: v.attr["coordinates"][0],vertices))
        yVals = list(map(lambda v: v.attr["coordinates"][1],vertices))

        xDist = max(xVals) - min(xVals)
        yDist = max(yVals) - min(yVals)

        if xDist > yDist:
            if xDist > len:
                len = xDist
        else:
            if yDist > len:
                len = yDist


    #convert all coordinates to values, relative to the resistor
    for vertex in graph.ve.values():
        x = vertex.attr["coordinates"][0]
        y = vertex.attr["coordinates"][1]
        vertex.attr["coordinates"] = [80*x/len,80*y/len]
    return graph

def snapCoordinatesToGrid(graph):
    gridSize = 32*1
    for vertex in graph.ve.values():
        x = math.floor(vertex.attr["coordinates"][0]/gridSize)*gridSize
        y = math.floor(vertex.attr["coordinates"][1]/gridSize)*gridSize
        vertex.attr["coordinates"] = [x,y]
    return graph

def seperateBuildingPartsAndConnection(buildingPartDefinitons,graph):
    #Get all the vertices connected to a building part
    for buildingPart in buildingPartDefinitons:
        vertices = buildingPart[2]
        rotation = buildingPart[1]
        type_ = buildingPart[0]

        #get all intersections
        intersectionVertices = list (filter(lambda v: v.color == INTERSECTION_COLOR,vertices) )

        #match LTSpice Model connections with graph Model connections
        connectionMap = {}
        connectionMap = CLASS_OBJECTS[type_].connect(rotation,intersectionVertices)

        #get center of the component
        xVals = list(map(lambda v: v.attr["coordinates"][0],vertices))
        yVals = list(map(lambda v: v.attr["coordinates"][1],vertices))

        xDist = max(xVals) - min(xVals)
        yDist = max(yVals) - min(yVals)
        center = [min(xVals)+xDist/2,min(yVals)+yDist/2]

        #collect all the vertices that need to be grouped
        vertexGroup = []
        for vertex in vertices:
            if vertex.color == INTERSECTION_COLOR:
                continue
            vertexGroup.append(vertex)

        component = Vertex(
                color=COMPONENT_COLOR,
                label=type_,
                attr={"connectionMap":connectionMap,"type":type_,"coordinates":center,"rotation":rotation}
            )
        #group
        graph.group(vertexGroup,component)

        #remove all direct connection between all Intersection Colors
        for vertex1 in vertices:
            if not vertex1.color == INTERSECTION_COLOR: continue
            for vertex2 in vertices:
                if not vertex2.color == INTERSECTION_COLOR: continue
                if vertex1 == vertex2: continue
                edge = graph.getEdgeBetweenVertices(vertex1.id,vertex2.id)
                if edge: graph.deleteEdge(edge.id)

    return graph

def alignVertices(graph):
    #pick Start Vertex
    startVertex = None
    for vertex in graph.ve.values():
        if vertex.color == CORNER_COLOR:
            startVertex = vertex
            break

    def traversial(graph,func,startV):
        def recursiveTraversial(currentV, lastV):
            if(not "passes" in currentV.attr.keys()): currentV.attr["passes"] = 0
            if(currentV.attr["passes"] == 3): return
            currentV.attr["passes"] += 1
            currentV = func(currentV,lastV)
            neighbors = graph.getNeighbors(currentV.id)
            for neighbor in neighbors:
                if neighbor == lastV: continue
                recursiveTraversial(neighbor,currentV)

        recursiveTraversial(startV,startV)

    def func(currentV,lastV):
        #get main Direction
        mainDir = "y"
        c_xPos = currentV.attr["coordinates"][0]
        c_yPos = currentV.attr["coordinates"][1]

        l_xPos = lastV.attr["coordinates"][0]
        l_yPos = lastV.attr["coordinates"][1]

        mainDir =  "x" if abs(c_xPos - l_xPos) > abs(c_yPos - l_yPos) else "y"

        #the other direction has to corrected
        if mainDir == "x":
            c_yPos = l_yPos

        if mainDir == "y":
            c_xPos = l_xPos

        currentV.attr["coordinates"] = [c_xPos,c_yPos]
        return currentV

    traversial(graph,func,startVertex)
    return graph

def insertConnectionNodes(graph):
    #for every Edge
    #freeze graph
    frozenGraph = copy.deepcopy(graph)
    for edge in frozenGraph.ed.values():

        #get Vertices connected to Edge
        vertices = graph.getVerticesForEdge(edge.id)

        #insert Connection Vertex
        connection = Vertex(
            color=CONNECTION_COLOR,
            label="con",
            attr={
                "from"  :vertices[0].attr["coordinates"],
                "to"    :vertices[1].attr["coordinates"],
            }
        )
        graph.insertVertexByEdge(edge.id,connection)
    return graph

def generateFile(graph,fileName):
    width,height = 1000,1000
    def generateWire(connectionVertex):
        from_ = connectionVertex.attr["from"]
        to_ = connectionVertex.attr["to"]
        text = "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(from_[0]),y1 =int(from_[1]),x2=int(to_[0]),y2=int(to_[1]))
        return text

    string = "Version 4\nSHEET 1 {w} {h}\n".format(w=width,h=height)
    for vertex in graph.ve.values():
        if not vertex.color == COMPONENT_COLOR: continue
        string += CLASS_OBJECTS[vertex.attr["type"]].generate(vertex)

    for vertex in graph.ve.values():
        if not vertex.color == CONNECTION_COLOR: continue
        string += generateWire(vertex)

    file = open(fileName,"w")
    file.write(string)
    file.close()

def createLTSpiceFile(predictions,graph,fileName):
    map = []
    for i in range(0, len(predictions)):
        map.append((predictions[i][2],predictions[i][3],predictions[i][1]))
    graph = recolorCap(graph)
    graph = toRelative(map,graph)
    graph = seperateBuildingPartsAndConnection(map,graph)
    graph = alignVertices(graph)
    graph = insertConnectionNodes(graph)
    generateFile(graph,fileName)


