from lib.utils import fmap
from math import dist
import drawSvg as draw

from lib.components.baseComponent import BaseComponent

#             |
# #0----------|
#             |
class Ground(BaseComponent):

    @staticmethod
    def connect(rotation,intersectionVertices):
        mapings = {0: intersectionVertices[0] }

        return mapings
    
    @staticmethod
    def getRotation(vertices, ROTATION_DICT):
        return ROTATION_DICT['up']
    
    @staticmethod
    def draw(groundVertex,wWidth,wHeight,d):

        groundSize = 15
        position = groundVertex.attr["connectionMap"][0]

        d.append(draw.Lines(
            position[0]             ,wHeight-position[1], 
            position[0]-groundSize  ,wHeight-position[1]
            ,stroke="#ff4477"
        ))
        d.append(draw.Lines(
            position[0]             ,wHeight-position[1],
            position[0]+groundSize  ,wHeight-position[1],
            stroke="#ff4477"
        ))

    @staticmethod
    def generate(groundVertex):
        position = groundVertex.attr["coordinates"]
        to = groundVertex.attr["connectionMap"][0].attr["coordinates"]
        text = "FLAG {x} {y} 0\n".format(x=int(position[0]),y=int(position[1]))
        text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]),y1=int(position[1]),x2=int(to[0]),y2=int(to[1]))
        return text