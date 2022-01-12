from lib.utils import fmap
from math import dist

from lib.components.baseComponent import BaseComponent

#        |-------------|
# #0-----|             |--------#1
#        |-------------|
class Resistor(BaseComponent):

    @staticmethod
    def connect(rotation,intersectionVertices):
        
        basePos = BaseComponent().getMeasurePoint(0,rotation,intersectionVertices)
    
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