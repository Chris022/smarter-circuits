from copy import deepcopy
from math import dist,hypot

from lib.constants import *

from lib.graphLib.vertex import Vertex
from lib.graphLib.edge import Edge
from lib.graphLib.graph import Graph


class Capacitor():
    @classmethod
    def pattern(self):
        cap = Graph()
        v1 = Vertex(color=END_COLOR)
        v2 = Vertex(color=OTHER_NODE_COLOR)
        v3 = Vertex(color=END_COLOR)
        cap.addVertices([v1,v2,v3])
        cap.addEdge(Edge(), v1.id, v2.id)
        cap.addEdge(Edge(), v3.id, v2.id)

        v4 = Vertex(color=END_COLOR)
        v5 = Vertex(color=OTHER_NODE_COLOR)
        v6 = Vertex(color=END_COLOR)
        cap.addVertices([v4,v5,v6])
        cap.addEdge(Edge(), v4.id, v5.id)
        cap.addEdge(Edge(), v6.id, v5.id)

        cap.addEdge(Edge(color=OTHER_EDGE_COLOR), v2.id, v5.id)
        return cap

    @classmethod
    def subPattern(self):
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

    # Takes a Graph
    # Searches the Graph for Grounds
    # checks if the "center" of a Ground is close to the "center" of another
    # It then checks if there is more than one other Note between the two Intersections (To avoid the connection of 2 close tougheter Caps)
    # if they are, the two Intersections are replaced with Other-Notes
    # and they get connected by a Other Line
    # returns: the modified Graph
    @classmethod
    def graphModification(self,graph):
        groundGraph = self.subPattern()

        # Match all ground Symbols
        groundMatches = graph.getPatternMatches(groundGraph)

        up = []
        down = []
        left = []
        right = []
        for groundMatchVertices in groundMatches:

            intersectionVertex = None
            for match in groundMatchVertices:
                if match.color == INTERSECTION_COLOR:
                    intersectionVertex = match

            neighborVertices = graph.getNeighbors(intersectionVertex.id)

            for neighborVertex in neighborVertices:
                if not neighborVertex.color == 'blue':

                    xOff = intersectionVertex.attr['coordinates'][0] - neighborVertex.attr['coordinates'][0]
                    yOff = intersectionVertex.attr['coordinates'][1] - neighborVertex.attr['coordinates'][1]

                    if abs(xOff) > abs(yOff):
                        if xOff > 0:
                            left.append(intersectionVertex)
                        else:
                            right.append(intersectionVertex)
                    else:
                        if yOff > 0:
                            up.append(intersectionVertex)
                        else:
                            down.append(intersectionVertex)
                    break

        for lCap in left:
            lCoord = lCap.attr['coordinates']

            rCoord = right[0].attr['coordinates']
            minDist = hypot(lCoord[0]-rCoord[0], lCoord[1]-rCoord[1])
            minCap = right[0]

            for rCap in right:
                rCoord = rCap.attr['coordinates']
                dist = hypot(lCoord[0]-rCoord[0], lCoord[1]-rCoord[1])

                if dist < minDist and graph.adjacent(lCap.id, rCap.id) == False:
                    minDist = dist
                    minCap = rCap

            lCap.color = OTHER_NODE_COLOR
            minCap.color = OTHER_NODE_COLOR
            graph.addEdge(Edge(color=OTHER_EDGE_COLOR),lCap.id, minCap.id)

        for dCap in down:
            dCoord = dCap.attr['coordinates']

            uCoord = up[0].attr['coordinates']
            minDist = hypot(dCoord[0]-uCoord[0], dCoord[1]-uCoord[1])
            minCap = up[0]

            for uCap in up:
                uCoord = uCap.attr['coordinates']
                dist = hypot(dCoord[0]-uCoord[0], dCoord[1]-uCoord[1])

                if dist < minDist and graph.adjacent(dCap.id, uCap.id) == False:
                    minDist = dist
                    minCap = uCap

            dCap.color = OTHER_NODE_COLOR
            minCap.color = OTHER_NODE_COLOR
            graph.addEdge(Edge(color=OTHER_EDGE_COLOR),dCap.id, minCap.id)

        return graph

    def match(self,graph):
        #call pre matching algorithms
        graph = self.graphModification(graph)
        #do matching
        graph = deepcopy(graph)
        return graph.getPatternMatches(self.pattern())