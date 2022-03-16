from copy import deepcopy

from lib.constants import *

from lib.graphLib.vertex import Vertex
from lib.graphLib.edge import Edge
from lib.graphLib.graph import Graph

class Ground():

    def pattern(self):
        ground = Graph()
        v1 = Vertex(color=END_COLOR)
        v2 = Vertex(color=INTERSECTION_COLOR)
        v3 = Vertex(color=END_COLOR)
        ground.addVertex(v1)
        ground.addVertex(v2)
        ground.addVertex(v3)
        ground.addEdge(Edge(), v1.id, v2.id)
        ground.addEdge(Edge(), v3.id, v2.id)
        return ground

    def match(self,graph):
        graph = deepcopy(graph)
        return graph.getPatternMatches(self.pattern())