import xml.etree.ElementTree as xml
import igraph

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

    def getVertex(self, id):
        return self.ve[id]

    def getEdge(self, id):
        return self.ed[id]

    def addVertex(self,vertex):
        vertex.__setId__(self.veIdCounter)
        self.veIdCounter +=1

        self.ve[vertex.id] = vertex
        self.incidenceMatrix.addRow(vertex.id)
    
    def addEdge(self,edge,from_,to_):
        edge.__setId__(self.veIdCounter)
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
    
    def adjacent(self,vertex1,vertex2):
        v1Index = self.incidenceMatrix.rows.index(vertex1)
        v2Index = self.incidenceMatrix.rows.index(vertex2)

        for column in self.incidenceMatrix.columns:
            edge = self.incidenceMatrix.getColumn(column)
            if edge[v1Index] > 0 and edge[v2Index] > 0:
                return True
        return False

    def getNeighbors(self,vertex):
        vertexIndex = self.incidenceMatrix.rows.index(vertex)
        neighbors = []
        for column in self.incidenceMatrix.columns:
            edge = self.incidenceMatrix.getColumn(column)
            if edge[vertexIndex] == 2:
                neighbors.append(vertex)
            elif edge[vertexIndex] == 1:
                edge[vertexIndex] = 0
                neighbors.append(self.incidenceMatrix.rows[edge.index(1)])

        return neighbors

    def verticesForEdge(self,edgeId):
        verticesList = []
        collectionValues = self.incidenceMatrix.getColumn(edgeId)
        vertices = self.incidenceMatrix.rows

        con = zip(collectionValues,vertices)
        for pair in con:
            if pair[0] == 1:
                verticesList.append(pair[1])
            if pair[0] == 2:
                verticesList = [pair[1],pair[1]]
        return verticesList

    def convertToIGraph(self):

        xmlns = xml.Element("graphml")

        key1 = xml.SubElement(xmlns,"key")
        key1.attrib= {"id":"v_name","for":"node","attr.name":"name","attr.type":"string"}
        key2 = xml.SubElement(xmlns,"key")
        key2.attrib= {"id":"v_color","for":"node","attr.name":"color","attr.type":"string"}
        key3 = xml.SubElement(xmlns,"key")
        key3.attrib= {"id":"v_label","for":"node","attr.name":"label","attr.type":"string"}
        key4 = xml.SubElement(xmlns,"key")
        key4.attrib= {"id":"e_color","for":"edge","attr.name":"color","attr.type":"string"}

        graph = xml.SubElement(xmlns, "graph")
        graph.attrib = {"id":"G","edgedefault":"undirected"}

        #add nodes
        for vertex in (self.ve).values():
            node = xml.SubElement(graph,"node")
            node.attrib = {"id":"n"+str(vertex.id)}

            data1 = xml.SubElement(node,"data")
            data1.attrib = {"key":"v_name"}
            data1.text = str(vertex.label)

            data2 = xml.SubElement(node,"data")
            data2.attrib = {"key":"v_color"}
            data2.text = str(vertex.color)

            data3 = xml.SubElement(node,"data")
            data3.attrib = {"key":"v_label"}
            data3.text = str(vertex.label)

        #add edges
        for e in (self.ed).values():
            edge = xml.SubElement(graph,"edge")
            verticeIds = self.verticesForEdge(e.id)
            edge.attrib = {"source":"n"+str(verticeIds[0]),"target":"n"+str(verticeIds[1])}

            data1 = xml.SubElement(edge,"data")
            data1.attrib = {"key":"e_color"}
            data1.text = str(e.color)

        xml_str = xml.tostring(xmlns, encoding='unicode')

        return '<?xml version="1.0" encoding="UTF-8"?>\n'+xml_str


g = Graph()

v1 = Vertex()
v2 = Vertex()
v3 = Vertex()

g.addVertex(v1)
g.addVertex(v2)
g.addVertex(v3)


e1 = Edge()
e2 = Edge()

g.addEdge(e1, v1.id, v2.id)
g.addEdge(e2, v1.id, v3.id)

print(g.adjacent(v1.id,v2.id))
print(g.adjacent(v2.id,v3.id))

print(g.getNeighbors(v3.id))