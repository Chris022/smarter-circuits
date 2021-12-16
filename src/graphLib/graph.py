from edge import Edge
from vertex import Vertex
from incidenceMatrix import IncidenceMatrix


class Graph:
    veIdCounter = 0
    ve = {}   # type_: {id:Vertex}
    edIdCounter = 0
    ed = {}   # type_: {id:Edge}

    incidenceMatrix = None

    def __init__(self) -> None:
        self.incidenceMatrix = IncidenceMatrix()

    def addVertex(self,vertex):
        vertex.__setId(self.veIdCounter)
        self.veIdCounter +=1

        self.ve[vertex.id] = vertex
        self.incidenceMatrix.addRow(vertex.id)
    
    def addEdge(self,edge,from_,to_):
        edge.__setId(self.veIdCounter)
        self.veIdCounter +=1

        self.ed[edge.id] = edge
        self.incidenceMatrix.addColumn(edge.id)
        #From
        self.incidenceMatrix.addValue(from_,edge.id)
        #To
        self.incidenceMatrix.addValue(to_,edge.id)

    def deleteEdge(self,edgeId):
        del self.ed[edgeId]
        self.incidenceMatrix.deleteColumn(edgeId)
    
    def deleteVertex(self,vertexId):
        del self.vs[vertexId]
        self.incidenceMatrix.deleteRow(vertexId)

        for edge in (self.ed).values():
            numOfConnectedVertices = sum(self.incidenceMatrix.getColumn(edge))
            if numOfConnectedVertices <= 1:
                self.deleteEdge(edge)
    
    def convertToIGraph(self):
        pass