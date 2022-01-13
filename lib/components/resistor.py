from math import dist
from lib.components.baseComponent import BaseComponent,getMeasurePoint

import drawSvg as draw

#        |-------------|
# #0-----|             |--------#1
#        |-------------|
class Resistor(BaseComponent):

    ltSpiceResistorWidth = 20
    resistorHeight = 20
    relativityValue = 40

    @staticmethod
    def connect(rotation,intersectionVertices):
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
    def draw(resistorVertex,rel,wWidth,wHeight,d):
        resW = rel
        resH = 20
        position = resistorVertex.attr["coordinates"]
        rotation = resistorVertex.attr["rotation"]

        #connect Resistor to connectionpoints
        to1 = resistorVertex.attr["connectionMap"][0]

        to2 = resistorVertex.attr["connectionMap"][1]

        if rotation == 0 or rotation == 180:
            d.append(draw.Rectangle(
                position[0]*rel-resW/2 ,wHeight-position[1]*rel-resH/2
                ,resW,resH,
                fill='none'
            ))
            d.append(draw.Lines(
                position[0]*rel-resW/2,     wHeight-position[1]*rel,
                to1[0]*rel,                 wHeight-to1[1]*rel ,
            ))
            d.append(draw.Lines(
                position[0]*rel+resW/2,     wHeight-position[1]*rel,
                to2[0]*rel,                 wHeight-to2[1]*rel
            ))
        elif rotation == 90 or rotation == 270:
            d.append(draw.Rectangle(
                position[0]*rel-resH/2,     wHeight-position[1]*rel-resW/2,
                resH,   resW,
                stroke='#1248ff',
                fill='none'
            ))

            d.append(draw.Lines(
                position[0]*rel,    wHeight-(position[1]*rel-resW/2),
                to1[0]*rel,         wHeight-to1[1]*rel
                ,stroke="#ff4477"
            ))
            d.append(draw.Lines(
                position[0]*rel,    wHeight-(position[1]*rel+resW/2),
                to2[0]*rel,         wHeight-to2[1]*rel ,
                stroke="#ff4477"
            ))

    @staticmethod
    def generate(resistorVertex,rel):
        rotation = resistorVertex.attr["rotation"]
        position = resistorVertex.attr["coordinates"]

        if rotation == 0 or rotation == 180:
            text = "SYMBOL Misc\\EuropeanResistor {x} {y} R90\n".format(x=int(position[0]*rel+56),y=int(position[1]*rel-16))
        else:
            text = "SYMBOL Misc\\EuropeanResistor {x} {y} R90\n".format(x=int(position[0]*rel+56),y=int(position[1]*rel-16))
        return text