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

    # Graph-Pattern of the Component
    @classmethod
    @abstractmethod
    def graphPattern(cls):
        pass

    # Gets called before Pattern mathing, does not change the original Graph!
    @classmethod
    def prePatternMatching(cls,graph):
        return graph

    # Gets called when the Graph is generated, does change the original Graph!
    @classmethod
    def graphModification(cls,graph):
        return graph

    #returns all matches with this component
    @classmethod
    def match(cls,graph):
        graph = deepcopy(graph)
        graph = cls.prePatternMatching(graph)
        return graph.getPatternMatches(cls.graphPattern())

    #takes a graph and returns a list of Lists with Vertices that belong to a occurrence of the component
    #returns := [Occurrance1,Occurrance2,...]
    #Occurrance := [Vertex1,Vertex2,Vertex3,...]
    #def findOccurrences(graph):
    #    graph.getPatternMatches(graphPattern())

#remove duplicate Mapping
def removeDuplicateMappings(mappings):
    def compairMapping(mapping1,mapping2):
        idSet1 = set()
        for m in mapping1:
            idSet1.add(m.id)
        idSet2 = set()
        for m in mapping2:
            idSet2.add(m.id)
        return idSet1 == idSet2
    newlist = []
    for mapping in mappings:
        add = True
        for el in newlist:
            if compairMapping(el,mapping):
                add = False
        if add:
            newlist.append(mapping)
    return newlist


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