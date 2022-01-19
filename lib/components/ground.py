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
        mapings = {0: intersectionVertices[0].attr["coordinates"] }

        return mapings
    
    @staticmethod
    def draw(groundVertex,rel,wWidth,wHeight,d):

        groundSize = 15
        position = groundVertex.attr["connectionMap"][0]

        d.append(draw.Lines(
            position[0]*rel             ,wHeight-position[1]*rel, 
            position[0]*rel-groundSize  ,wHeight-position[1]*rel
            ,stroke="#ff4477"
        ))
        d.append(draw.Lines(
            position[0]*rel             ,wHeight-position[1]*rel,
            position[0]*rel+groundSize  ,wHeight-position[1]*rel,
            stroke="#ff4477"
        ))

    @staticmethod
    def generate(groundVertex,rel):
        position = groundVertex.attr["coordinates"]
        text = "FLAG {x} {y} 0\n".format(x=int(position[0]*rel-40),y=int(position[1]*rel))
        return text