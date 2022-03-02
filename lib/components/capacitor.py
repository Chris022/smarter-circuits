from math import dist,hypot
from lib.components.baseComponent import BaseComponent,getMeasurePoint
from lib.components.ground import Ground
from lib.constants import *
from lib.graphLib.vertex import Vertex
from lib.graphLib.edge import Edge
from lib.graphLib.graph import Graph

#        |    |
# #0-----|    |--------#1
#        |    |
class Capacitor(BaseComponent):

    @classmethod
    def connect(cls,rotation,intersectionVertices):
        if rotation == 0 or 180:
            rotation = 0
        else:
            rotation = 90
        basePos = getMeasurePoint(0,rotation,intersectionVertices)
    
        #now get the distance from the (x|y) point to each intersection
        #and map the smalles to connection 0, the second smallest to 1 ...
        distances = []
        for intersectionVertex in intersectionVertices:
            position = intersectionVertex.attr["coordinates"]
            
            distance = dist(basePos,position)
            distances.append((distance,intersectionVertex))

        #sort distances
        mapings = map(lambda x: x[1], sorted(distances, key=lambda x:x[0]))

        #convert to map
        mapings = dict(enumerate(mapings)) 
        
        return mapings

    @classmethod
    def getRotation(cls,vertices, ROTATION_DICT):
        intersections = []
        for vertex in vertices:
            if vertex.color != 'blue' and vertex.color != 'yellow':
                intersections.append(vertex)
        if len(intersections) > 2:
            print('Too much intersections in capacitor')
        pos1 = intersections[0].attr['coordinates']
        pos2 = intersections[1].attr['coordinates']

        xDiff = abs(pos1[0]-pos2[0])
        yDiff = abs(pos1[1]-pos2[1])

        if xDiff > yDiff:
            return ROTATION_DICT['left']
        if yDiff > xDiff:
            return ROTATION_DICT['up']

        return -1


    @classmethod
    def toLTSpice(cls,resistorVertex,counter):
        rotation = resistorVertex.attr["rotation"]
        position = resistorVertex.attr["coordinates"]

        toVertex1 = resistorVertex.attr["connectionMap"][0]
        toVertex2 = resistorVertex.attr["connectionMap"][1]

        to1 = toVertex1.attr["coordinates"]
        to2 = toVertex2.attr["coordinates"]

        if toVertex1.color == COMPONENT_COLOR:
            to1 = [position[0]+(to1[0]-position[0])/2,position[1]+(to1[1]-position[1])/2]

        if toVertex2.color == COMPONENT_COLOR:
            to2 = [position[0]+(to2[0]-position[0])/2,position[1]+(to2[1]-position[1])/2]

        if rotation == 0 or rotation == 180:
            text = "SYMBOL cap {x} {y} R90\n".format(x=int(position[0]+32),y=int(position[1]-16))
            text += "SYMATTR InstName C{n}\n".format(n=counter)
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]-32),y1=int(position[1]),x2=int(to1[0]),y2=int(to1[1]))
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]+32),y1=int(position[1]),x2=int(to2[0]),y2=int(to2[1]))
        else:
            text = "SYMBOL cap {x} {y} R0\n".format(x=int(position[0]-16),y=int(position[1]-32))
            text += "SYMATTR InstName C{n}\n".format(n=counter)
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]),y1=int(position[1]-32),x2=int(to1[0]),y2=int(to1[1]))
            text += "WIRE {x1} {y1} {x2} {y2}\n".format(x1=int(position[0]),y1=int(position[1]+32),x2=int(to2[0]),y2=int(to2[1]))
        return text

    @classmethod
    def graphPattern(cls):
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


    # Takes a Graph
    # Searches the Graph for Grounds
    # checks if the "center" of a Ground is close to the "center" of another
    # It then checks if there is more than one other Note between the two Intersections (To avoid the connection of 2 close tougheter Caps)
    # if they are, the two Intersections are replaced with Other-Notes
    # and they get connected by a Other Line
    # returns: the modified Graph
    @classmethod
    def graphModification(cls,graph):
        groundGraph = Ground().graphPattern()

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