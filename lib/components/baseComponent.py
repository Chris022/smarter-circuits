from abc import ABC, abstractmethod
from lib.utils import fmap


class BaseComponent(ABC):

    @staticmethod
    @abstractmethod
    def connect(rotation,intersectionVertices):
        pass


    # Functon that generates the LT-Spice Code for the Component and returns it as a string
    @staticmethod
    @abstractmethod
    def toLTSpice(vertex):
        pass

    # Graph-Pattern of the Component
    @staticmethod
    @abstractmethod
    def graphPattern():
        pass

    # Gets called before Pattern mathing, does not change the original Graph!
    @staticmethod
    def prePatternMatching(graph):
        return graph

    # Gets called when the Graph is generated, does change the original Graph!
    @staticmethod
    def graphModification(graph):
        return graph

    #takes a graph and returns a list of Lists with Vertices that belong to a occurrence of the component
    #returns := [Occurrance1,Occurrance2,...]
    #Occurrance := [Vertex1,Vertex2,Vertex3,...]
    #def findOccurrences(graph):
    #    graph.getPatternMatches(graphPattern())


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