from math import dist
from turtle import pos
from lib.components.baseComponent import BaseComponent,getMeasurePoint

from lib.constants import *
from lib.graphLib.vertex import Vertex
from lib.graphLib.edge import Edge
from lib.graphLib.graph import Graph

#        |-------------|
# #0-----|=============|--------#1
#        |-------------|
class Inductor(BaseComponent):

    ltSpiceInductorWidth = 20
    InductorHeight = 20
    relativityValue = 40

    @staticmethod
    def connect(rotation,intersectionVertices):
        if rotation == 0 or 180:
            rotation = 0
        else:
            rotation = 90
        basePos = getMeasurePoint(0,rotation,intersectionVertices)
    
        #now get the distance from the (x|y) point to each intersection
        #and map the smalles to connection 0, the second smallest to 1 ...
        distances = []
        for intersectionVertex in intersectionVertices:
            position = intersectionVertex.attr["coordinates"]
            
            distance = dist(basePos,position)
            distances.append((distance,intersectionVertex))

        #sort distances
        mapings = map(lambda x: x[1], sorted(distances, key=lambda x:x[0]))

        #convert to map
        mapings = dict(enumerate(mapings)) 
        
        return mapings

    @staticmethod
    def getRotation(vertices, ROTATION_DICT):
        intersections = []
        for vertex in vertices:
            if vertex.color == 'red':
                intersections.append(vertex)
        if len(intersections) > 2:
            print('Too much intersections in resistor')
        pos1 = intersections[0].attr['coordinates']
        pos2 = intersections[1].attr['coordinates']

        xDiff = abs(pos1[0]-pos2[0])
        yDiff = abs(pos1[1]-pos2[1])

        if xDiff > yDiff:
            return ROTATION_DICT['left']
        if yDiff > xDiff:
            return ROTATION_DICT['up']

        return -1

    @staticmethod
    def draw(inductorVertex,wWidth,wHeight,d):
        pass

    @staticmethod
    def generate(inductorVertex, counter):
        rotation = inductorVertex.attr["rotation"]
        position = inductorVertex.attr["coordinates"]

        toVertex1 = inductorVertex.attr["connectionMap"][0]
        toVertex2 = inductorVertex.attr["connectionMap"][1]

        to1 = toVertex1.attr["coordinates"]
        to2 = toVertex2.attr["coordinates"]

        if toVertex1.color == "green":
            to1 = [position[0]+(to1[0]-position[0])/2,position[1]+(to1[1]-position[1])/2]

        if toVertex2.color == "green":
            to2 = [position[0]+(to2[0]-position[0])/2,position[1]+(to2[1]-position[1])/2]

        if rotation == 0 or rotation == 180:
            text = "SYMBOL ind {x} {y} R90\n".format(x=int(position[0]+56),y=int(position[1]-16))
            text += "SYMATTR InstName L{n}\n".format(n=counter)
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]-40),y1=int(position[1]),x2=int(to1[0]),y2=int(to1[1]))
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]+40),y1=int(position[1]),x2=int(to2[0]),y2=int(to2[1]))
        else:
            text = "SYMBOL ind {x} {y} R0\n".format(x=int(position[0]-16),y=int(position[1]-56))
            text += "SYMATTR InstName L{n}\n".format(n=counter)
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]),y1=int(position[1]-40),x2=int(to1[0]),y2=int(to1[1]))
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]),y1=int(position[1]+40),x2=int(to2[0]),y2=int(to2[1]))
        return text

    @staticmethod
    def graphPattern():
        ind = Graph()
        v1 = Vertex(color=INTERSECTION_COLOR)
        v2 = Vertex(color=CORNER_COLOR)
        v3 = Vertex(color=CORNER_COLOR)
        v4 = Vertex(color=INTERSECTION_COLOR)
        v5 = Vertex(color=CORNER_COLOR)
        v6 = Vertex(color=CORNER_COLOR)
        ind.addVertices([v1,v2,v3,v4,v5,v6])
        ind.addEdge(Edge(), v1.id, v2.id)
        ind.addEdge(Edge(), v2.id, v3.id)
        ind.addEdge(Edge(), v3.id, v4.id)
        ind.addEdge(Edge(), v4.id, v5.id)
        ind.addEdge(Edge(), v5.id, v6.id)
        ind.addEdge(Edge(), v6.id, v1.id)
        return ind