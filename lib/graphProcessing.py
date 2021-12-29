import math
from lib.graphLib.vertex import Vertex

def combineCloseVertices(graph,vertices, thresholdDistance):
    #array that holds vertices that were already combine
    alreadyCombined = []
    #start by finding close vertices
    for vertex1 in vertices:
        #if vertex is already combinde -> skipp
        if vertex1 in alreadyCombined:
            continue

        toCombineVertices = [vertex1]
        for vertex2 in vertices:
            #don't compair if both vertices are the same
            if vertex1 == vertex2 or vertex2 in alreadyCombined:
                continue
            #get dist between vertices
            pos1 = vertex1.attr["coordinates"]
            pos2 = vertex2.attr["coordinates"]

            dist = math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

            if dist > thresholdDistance:
                continue
            #if dist smaller than thrashhold -> combine vertices
            toCombineVertices.append(vertex2)
            alreadyCombined.append(vertex2)

        # only combine vertices if there are more than one
        if len(toCombineVertices) <= 1:
            continue
            
        # create replacementVertex
        repV = Vertex(  
                        color=vertex1.color,
                        label=vertex1.label,
                        attr=dict(vertex1.attr)
                    )

        graph.group(toCombineVertices,repV)
    return graph

