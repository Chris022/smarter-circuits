from math import dist
from lib.components.components.baseComponent import BaseComponent,getMeasurePoint

from lib.constants import *
from lib.graphLib.vertex import Vertex
from lib.graphLib.edge import Edge
from lib.graphLib.graph import Graph


#        |-------------|
# #0-----|-------------|--------#1
#        |-------------|
class Voltage(BaseComponent):

    @classmethod
    def connect(cls,rotation,intersectionVertices):
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

    @classmethod
    def getRotation(cls,vertices, ROTATION_DICT):
        intersections = []
        for vertex in vertices:
            if vertex.color == 'red':
                intersections.append(vertex)
        if len(intersections) > 2:
            print('Too much intersections in voltage source')
        if len(intersections) < 2:
            print('Not enough intersections in voltage source')
            return -1
        pos1 = intersections[0].attr['coordinates']
        pos2 = intersections[1].attr['coordinates']

        xDiff = abs(pos1[0]-pos2[0])
        yDiff = abs(pos1[1]-pos2[1])

        if xDiff > yDiff:
            return ROTATION_DICT['left']
        if yDiff > xDiff:
            return ROTATION_DICT['up']

        return -1

    @classmethod
    def toLTSpice(cls,resistorVertex,counter):
        rotation = resistorVertex.attr["rotation"]
        position = resistorVertex.attr["coordinates"]
        if len (resistorVertex.attr["connectionMap"]) !== 0:
            return ""
        toVertex1 = resistorVertex.attr["connectionMap"][0]
        toVertex2 = resistorVertex.attr["connectionMap"][1]

        to1 = toVertex1.attr["coordinates"]
        to2 = toVertex2.attr["coordinates"]

        if toVertex1.color == COMPONENT_COLOR:
            to1 = [position[0]+(to1[0]-position[0])/2,position[1]+(to1[1]-position[1])/2]

        if toVertex2.color == COMPONENT_COLOR:
            to2 = [position[0]+(to2[0]-position[0])/2,position[1]+(to2[1]-position[1])/2]

        if rotation == 0 or rotation == 180:
            text = "SYMBOL voltage {x} {y} R90\n".format(x=int(position[0]+56),y=int(position[1]))
            text += "SYMATTR InstName R{n}\n".format(n=counter)
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]-40),y1=int(position[1]),x2=int(to1[0]),y2=int(to1[1]))
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]+40),y1=int(position[1]),x2=int(to2[0]),y2=int(to2[1]))
        else:
            text = "SYMBOL voltage {x} {y} R0\n".format(x=int(position[0]),y=int(position[1]-56))
            text += "SYMATTR InstName R{n}\n".format(n=counter)
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]),y1=int(position[1]-40),x2=int(to1[0]),y2=int(to1[1]))
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]),y1=int(position[1]+40),x2=int(to2[0]),y2=int(to2[1]))
        return text
