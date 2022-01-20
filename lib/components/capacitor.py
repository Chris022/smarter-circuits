from math import dist
from lib.components.baseComponent import BaseComponent,getMeasurePoint

import drawSvg as draw

#        |-------------|
# #0-----|             |--------#1
#        |-------------|
class Capacitor(BaseComponent):

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
            distances.append((distance,position))

        #sort distances
        mapings = map(lambda x: x[1], sorted(distances, key=lambda x:x[0]))

        #convert to map
        mapings = dict(enumerate(mapings)) 
        
        return mapings

    @staticmethod
    def draw(capacitorVertex,wWidth,wHeight,d):
        pass

    @staticmethod
    def generate(resistorVertex):
        rotation = resistorVertex.attr["rotation"]
        position = resistorVertex.attr["coordinates"]

        to1 = resistorVertex.attr["connectionMap"][0]
        to2 = resistorVertex.attr["connectionMap"][1]

        if rotation == 0 or rotation == 180:
            text = "SYMBOL cap {x} {y} R90\n".format(x=int(position[0]+32),y=int(position[1]-16))
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]-32),y1=int(position[1]),x2=int(to1[0]),y2=int(to1[1]))
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]+32),y1=int(position[1]),x2=int(to2[0]),y2=int(to2[1]))
        else:
            text = "SYMBOL cap {x} {y} R0\n".format(x=int(position[0]-16),y=int(position[1]+32))
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]),y1=int(position[1]-32),x2=int(to2[0]),y2=int(to2[1]))
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]),y1=int(position[1]+32),x2=int(to1[0]),y2=int(to1[1]))
        return text