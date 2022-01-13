from lib.utils import fmap
from math import dist

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
    def draw():
        pass