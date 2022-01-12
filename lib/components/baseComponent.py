from abc import ABC, abstractmethod
from lib.utils import fmap


class BaseComponent(ABC):

    @staticmethod
    @abstractmethod
    def connect(rotation,intersectionVertices):
        pass

def getMeasurePoint(rotatonOffset, rotation,intersectionVertices):
    xPositions = fmap (lambda x: x.attr["coordinates"][0],intersectionVertices)
    yPositions = fmap (lambda x: x.attr["coordinates"][1],intersectionVertices)
    rot = rotatonOffset + rotation
    
    if      rot == 0:
        x = min(xPositions)
        y = min(yPositions)
        x -= 100
    elif    rot == 90:
        x = min(xPositions)
        y = max(yPositions)
        y += 100
    elif    rot == 180:
        x = max(xPositions)
        y = max(yPositions)
        x += 100
    elif    rot == 270:
        x = max(xPositions)
        y = min(yPositions)
        y -= 100
    return (x,y)