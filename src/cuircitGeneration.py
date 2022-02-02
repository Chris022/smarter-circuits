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
    len = 1000
    for buildingPart in buildingPartDefinitons:
        vertices = buildingPart[2]
        rotation = buildingPart[1]
        type_ = buildingPart[0]

        if type_ == CLASS_OBJECT_NAMES["gnd"]:
            continue
        
        xVals = list(map(lambda v: v.attr["coordinates"][0],vertices))
        yVals = list(map(lambda v: v.attr["coordinates"][1],vertices))

        xDist = max(xVals) - min(xVals)
        yDist = max(yVals) - min(yVals)


        if rotation == 0 or rotation == 180:
            if xDist < len and xDist < len:
                len = xDist
        else:
            if yDist < len and xDist < len:
                len = yDist

    #print(len)
    #convert all coordinates to values, relative to the resistor
    for vertex in graph.ve.values():
        x = vertex.attr["coordinates"][0]
        y = vertex.attr["coordinates"][1]
        vertex.attr["coordinates"] = [64*x/len,64*y/len]
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
        #rotation = buildingPart[1]
        type_ = buildingPart[0]

        rotation = CLASS_OBJECTS[type_].getRotation(vertices, ROTATION_DICT)

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

        #delete all vertices of the component accept the intersection points, change type to edge for them!
        for vertex in vertices:
            if vertex.color == INTERSECTION_COLOR:
                vertex.color = CORNER_COLOR
                continue
            graph.deleteVertex(vertex.id)
        #delete all green edges
        edges = list(graph.ed.values())
        for edge in edges:
            if edge.color == OTHER_EDGE_COLOR:
                graph.deleteEdge(edge.id)
        #add UNCONECTED component Vertex
        component = Vertex(
                color=COMPONENT_COLOR,
                label=type_,
                attr={"connectionMap":connectionMap,"type":type_,"coordinates":center,"rotation":rotation}
            )
        graph.addVertex(component)
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
    graph = snapCoordinatesToGrid(graph)
    graph = seperateBuildingPartsAndConnection(map,graph)
    graph = insertConnectionNodes(graph)
    generateFile(graph,fileName)


