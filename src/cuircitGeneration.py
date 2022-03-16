from copy import deepcopy
import math

import sys
sys.path.append('../')

import lib.graphLib.graph as g
from lib.graphLib.vertex import Vertex
from lib.graphLib.edge import Edge

from lib.constants import *
from lib.components.componentCollection import CLASS_OBJECTS
from lib.utils import convertToIgraph

import igraph

def toRelative(buildingPartDefinitons,graph):
    #get lenght of the longest resistor
    len = 80
    for buildingPart in buildingPartDefinitons:
        type_ = buildingPart[0]
        vertices = buildingPart[1]
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
    print("Biggest lenght of resistor " + str(len))
    #convert all coordinates to values, relative to the resistor
    for vertex in graph.ve.values():
        x = vertex.attr["coordinates"][0]
        y = vertex.attr["coordinates"][1]
        vertex.attr["unscaled"] = list(vertex.attr["coordinates"])
        vertex.attr["coordinates"] = [80*x/len*1.5,80*y/len*1.5] # also add a bit of spacing by multiplying *1.5
        
    return graph

def snapCoordinatesToGrid(graph):
    gridSize = 16
    for vertex in graph.ve.values():
        x = math.floor(vertex.attr["coordinates"][0]/gridSize)*gridSize
        y = math.floor(vertex.attr["coordinates"][1]/gridSize)*gridSize
        vertex.attr["coordinates"] = [x,y]
    return graph

def seperateBuildingPartsAndConnection(buildingPartDefinitons,graph):
    #Get all the vertices connected to a building part
    for buildingPart in buildingPartDefinitons:
        type_ = buildingPart[0]

        vertices = buildingPart[1]

        boundingBox = buildingPart[2]

        upperRightCorner = boundingBox[0]
        lowerLeftCorner = boundingBox[1]

        newGraph = deepcopy(graph)
        #TODO
        #newGraph = CLASS_OBJECTS[type_].prePatternMatching(newGraph)

        newVertices = []
        for vertex in vertices:
            try:
                newVertices.append(newGraph.getVertex(vertex.id))
            except:
                pass

        rotation = CLASS_OBJECTS[type_].getRotation(newVertices, ROTATION_DICT)

        #get center of the component
        xVals = list(map(lambda v: v.attr["coordinates"][0],vertices))
        yVals = list(map(lambda v: v.attr["coordinates"][1],vertices))

        xDist = max(xVals) - min(xVals)
        yDist = max(yVals) - min(yVals)
        center = [min(xVals)+xDist/2,min(yVals)+yDist/2]

        component = Vertex(
                color=COMPONENT_COLOR,
                label=type_,
                attr={"connectionMap":{},"type":type_,"coordinates":center,"unscaled":[-1,-1],"rotation":rotation}
        )
        #group
        graph.group(vertices,component)

        #remove all vertices in the bounding box, that is not the component
        allVertices = list(graph.ve.values())
        for v in allVertices:
            #check if coordinates are in the bounding box
            if upperRightCorner[0] < v.attr["unscaled"][0] and upperRightCorner[1] < v.attr["unscaled"][1]:
                if lowerLeftCorner[0] > v.attr["unscaled"][0] and lowerLeftCorner[1] > v.attr["unscaled"][1]:
                    #check if vertex isnt component vertex
                    if not v == component:
                        graph.deleteVertex(v.id)

    #remove all End points
    copy = list(graph.ve.values())
    for vertex in copy:
        if vertex.color == END_COLOR:
            graph.deleteVertex(vertex.id)
        

    for vertex in graph.ve.values():
        if not vertex.color == COMPONENT_COLOR: continue
        rotation = vertex.attr["rotation"]
        type_ = vertex.attr["type"]

        #set Connection Map
        #match LTSpice Model connections with graph Model connections
        connectionMap = CLASS_OBJECTS[type_].connect(rotation,graph.getNeighbors(vertex.id))
        vertex.attr["connectionMap"] = connectionMap

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
                #if "passes" in neighbor.attr.keys() and neighbor.attr["passes"] > currentV.attr["passes"]: continue
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
    frozenGraph = deepcopy(graph)
    for edge in frozenGraph.ed.values():
        #get Vertices connected to Edge
        vertices = graph.getVerticesForEdge(edge.id)

        #if one of the vertices is green -> ignore
        f = False
        for vertex in vertices:
            if vertex.color == COMPONENT_COLOR:
                f = True
        if f: continue

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
    counter = {}
    for key in CLASS_OBJECTS:
        counter.update({key:0})

    width,height = 1000,1000
    def generateWire(connectionVertex):
        from_ = connectionVertex.attr["from"]
        to_ = connectionVertex.attr["to"]
        text = "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(from_[0]),y1 =int(from_[1]),x2=int(to_[0]),y2=int(to_[1]))
        return text

    string = "Version 4\nSHEET 1 {w} {h}\n".format(w=width,h=height)
    for vertex in graph.ve.values():
        if not vertex.color == COMPONENT_COLOR: continue
        string += CLASS_OBJECTS[vertex.attr["type"]].toLTSpice(vertex, counter[vertex.attr["type"]])
        counter[vertex.attr["type"]] += 1
    for vertex in graph.ve.values():
        if not vertex.color == CONNECTION_COLOR: continue
        string += generateWire(vertex)

    file = open(fileName,"w")
    file.write(string)
    file.close()

def createLTSpiceFile(matches,boundingBoxes,predictions,graph,fileName):
    map = []
    for i in range(0, len(predictions)):
        map.append([predictions[i],matches[i],boundingBoxes[i]])
    graph = toRelative(map,graph)
    graph = seperateBuildingPartsAndConnection(map,graph)

    graph = snapCoordinatesToGrid(graph)
    graph = alignVertices(graph)
    generateFile(insertConnectionNodes(graph),fileName)
    return graph

    