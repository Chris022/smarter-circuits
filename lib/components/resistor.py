from lib.utils import fmap
from math import dist

from lib.components.baseComponent import BaseComponent

#        |-------------|
# #0-----|             |--------#1
#        |-------------|
class Resistor(BaseComponent):

    @staticmethod
    def connect(rotation,intersectionVertices):
        #get lowest Y and X coordinate
        xPositions = fmap (lambda x: x.attr["coordinates"][0],intersectionVertices)
        yPositions = fmap (lambda x: x.attr["coordinates"][1],intersectionVertices)
        x = min(xPositions)
        y = min(yPositions)

        # make the x direction smaler by 100
        x -= 100
    
        #now get the distance from the (x|y) point to each intersection
        #and map the smalles to connection 0, the second smallest to 1 ...
        distances = []
        for intersectionVertex in intersectionVertices:
            position = intersectionVertex.attr["coordinates"]
            
            distance = dist((x,y),position)
            distances.append((distance,position))

        #sort distances
        mapings = map(lambda x: x[1], sorted(distances, key=lambda x:x[0]))

        #convert to map
        mapings = dict(enumerate(mapings)) 
        
        return mapings