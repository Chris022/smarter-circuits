from copy import deepcopy

from lib.constants import *
from lib.utils import removeDuplicateMappings

from lib.graphLib.vertex import Vertex
from lib.graphLib.edge import Edge
from lib.graphLib.graph import Graph

class Resistor():

    def pattern(self):
        res = Graph()
        v1 = Vertex(color=INTERSECTION_COLOR)
        v2 = Vertex(color=INTERSECTION_COLOR)

        res.addVertices([v1,v2])
        res.addEdge(Edge(), v1.id, v2.id)
        res.addEdge(Edge(), v2.id, v1.id)

        return res

    def removePigTails(self,graph):
        copy2 = list(graph.ve.values())
        for ve in copy2:
            if ve.color == INTERSECTION_COLOR:
                neighbors = graph.getNeighbors(ve.id)
                for neib in neighbors:
                    if neib.color == END_COLOR:
                        graph.deleteVertex(neib.id)
                        if len(neighbors) == 3:
                            ve.color = CORNER_COLOR

        return graph

    def removeYellows(self,graph):
        #remove all yellows
        copy = list(graph.ve.values())
        for v in copy:
            if v.color == CORNER_COLOR:
                graph.removeVertex(v.id)

        return graph

    def match(self,graph):
        #Match first pattern
        graph1 = deepcopy(graph)
        graph1 = self.removeYellows(graph1) #only remove corners
        matches1 = graph1.getPatternMatches(self.pattern())

        #Match second pattern
        graph2 = deepcopy(graph)
        graph2 = self.removePigTails(graph2) #remove pigtails
        graph2 = self.removeYellows(graph2) #and remove corners
        matches2 = graph2.getPatternMatches(self.pattern())

        #Combine both
        mapings =  matches1 + matches2
        #remove mappings that were matched by both patterns
        mapings = removeDuplicateMappings(mapings)

        return mapings