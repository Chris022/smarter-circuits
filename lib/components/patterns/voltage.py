from copy import deepcopy

from lib.constants import *

from lib.graphLib.vertex import Vertex
from lib.graphLib.edge import Edge
from lib.graphLib.graph import Graph

class Voltage():

    def pattern(self):
        res = Graph()
        v1 = Vertex(color=INTERSECTION_COLOR)
        v2 = Vertex(color=INTERSECTION_COLOR)
        res.addVertices([v1,v2])
        res.addEdge(Edge(), v2.id, v1.id)
        res.addEdge(Edge(), v2.id, v1.id)
        res.addEdge(Edge(), v2.id, v1.id)

        return res

    def removeYellows(self,graph):
        #remove all yellows
        copy = list(graph.ve.values())
        for v in copy:
            if v.color == CORNER_COLOR:
                graph.removeVertex(v.id)
        return graph

    def match(self,graph):
        graph = deepcopy(graph)
        graph = self.removeYellows(graph)
        return graph.getPatternMatches(self.pattern())