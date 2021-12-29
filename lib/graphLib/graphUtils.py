import igraph
import os

def drawGraph(graph):
    f = open("out.graph", "w")
    f.write(graph.convertToIGraph())
    f.close()
    g = igraph.Graph().Read("out.graph",format="graphml")
    os.remove("out.graph") 
    layout = g.layout("fr")
    igraph.plot(g, layout=layout,bbox = (1000,1000))