from math import dist
from lib.components.components.baseComponent import BaseComponent,getMeasurePoint

from lib.constants import *

#        |-------------|
# #0-----|=============|--------#1
#        |-------------|
class Inductor(BaseComponent):

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
        mapings = reversed(list(map(lambda x: x[1], sorted(distances, key=lambda x:x[0]))))

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
            print('Too much intersections in inductor')
        if len(intersections) < 2:
            print('Not enough intersections in inductor')
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
    def toLTSpice(cls,inductorVertex, counter):
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