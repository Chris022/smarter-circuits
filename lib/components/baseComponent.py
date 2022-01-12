from abc import ABC, abstractmethod
from lib.constants import POSSIBLE_ROTATIONS
from lib.utils import fmap

class BaseComponent(ABC):

    @staticmethod
    def getMeasurePoint(rotatonOffset, rotation,intersectionVertices):
        xPositions = fmap (lambda x: x.attr["coordinates"][0],intersectionVertices)
        yPositions = fmap (lambda x: x.attr["coordinates"][1],intersectionVertices)
        rot = rotatonOffset + rotation
        if      rot == POSSIBLE_ROTATIONS[0]:
            x = min(xPositions)
            y = min(yPositions)

            x -= 100
        elif    rot == POSSIBLE_ROTATIONS[1]:
            x = min(xPositions)
            y = max(yPositions)

            y += 100
        elif    rot == POSSIBLE_ROTATIONS[3]:
            x = max(xPositions)
            y = max(yPositions)

            x += 100
        elif    rot == POSSIBLE_ROTATIONS[3]:
            x = max(xPositions)
            y = min(yPositions)

            y -= 100
        return (x,y)

    @staticmethod
    @abstractmethod
    def connect(rotation,intersectionVertices):
        pass