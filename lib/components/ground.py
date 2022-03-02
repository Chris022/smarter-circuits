from lib.utils import fmap
from math import dist

from lib.constants import *
from lib.graphLib.vertex import Vertex
from lib.graphLib.edge import Edge
from lib.graphLib.graph import Graph

from lib.components.baseComponent import BaseComponent

#             |
# #0----------|
#             |
class Ground(BaseComponent):

    @classmethod
    def connect(cls,rotation,intersectionVertices):
        mapings = {0: intersectionVertices[0] }

        return mapings
    
    @classmethod
    def getRotation(cls,vertices, ROTATION_DICT):
        return ROTATION_DICT['up']

    @classmethod
    def toLTSpice(cls,groundVertex,counter):
        position = groundVertex.attr["coordinates"]
        toVertex = groundVertex.attr["connectionMap"][0]
        to = toVertex.attr["coordinates"]

        if toVertex.color == COMPONENT_COLOR:
            to = [position[0]+(to[0]-position[0])/2,position[1]+(to[1]-position[1])/2]

        text = "FLAG {x} {y} 0\n".format(x=int(position[0]),y=int(position[1]))
        text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]),y1=int(position[1]),x2=int(to[0]),y2=int(to[1]))
        return text

    @classmethod
    def graphPattern(cls):
        ground = Graph()
        v1 = Vertex(color=END_COLOR)
        v2 = Vertex(color=INTERSECTION_COLOR)
        v3 = Vertex(color=END_COLOR)
        ground.addVertex(v1)
        ground.addVertex(v2)
        ground.addVertex(v3)
        ground.addEdge(Edge(), v1.id, v2.id)
        ground.addEdge(Edge(), v3.id, v2.id)
        return ground