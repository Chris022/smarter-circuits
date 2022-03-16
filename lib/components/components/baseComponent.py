from abc import ABC, abstractmethod
from lib.utils import fmap
from copy import deepcopy

class BaseComponent(ABC):

    @classmethod
    @abstractmethod
    def connect(cls,rotation,intersectionVertices):
        pass


    # Functon that generates the LT-Spice Code for the Component and returns it as a string
    @classmethod
    @abstractmethod
    def toLTSpice(cls,vertex):
        pass


#returns the point for connecting the Component, depending on its rotation
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