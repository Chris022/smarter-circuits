import xml.etree.ElementTree as xml
#import igraph

from edge import Edge
from vertex import Vertex
from table import Table


class Graph:

    def __init__(self) -> None:
        self.veIdCounter = 0
        self.ve = {}   # type_: {id:Vertex}
        self.edIdCounter = 0
        self.ed = {}   # type_: {id:Edge}
        self.table = Table()

    def getVertex(self, vertexId):
        return self.ve[vertexId]

    def getEdge(self, edgeId):
        return self.ed[edgeId]

    def addVertex(self, vertex):
        vertex.__setId__(self.veIdCounter)
        self.veIdCounter +=1

        self.ve[vertex.id] = vertex
        self.table.addRow(vertex.id)

    def addVertices(self, vertices):
        for vertex in vertices:
            vertex.__setId__(self.veIdCounter)
            self.veIdCounter +=1

            self.ve[vertex.id] = vertex
            self.tabel.addRow(vertex.id)
    
    def addEdge(self, edge, vertexId1, vertexId2):
        edge.__setId__(self.edIdCounter)
        self.edIdCounter +=1

        self.ed[edge.id] = edge
        self.tabel.addColumn(edge.id)
        #From
        self.tabel.addValue(vertexId1,edge.id)
        #To
        self.tabel.addValue(vertexId2,edge.id)

    def getVertices(self, edgeId):

        column = self.tabel.getColumn(edgeId)
        vertices = []
        for i in range(0, len(column)):
            if column[i] == 2:
                vertices.append(self.getVertex(self.tabel.rows[i]))
                vertices.append(self.getVertex(self.tabel.rows[i]))
            if column[i] == 1:
                vertices.append(self.getVertex(self.tabel.rows[i]))

        return vertices

    def deleteEdge(self, edgeId):
        del self.ed[edgeId]
        self.tabel.deleteColumn(edgeId)
    
    def deleteVertex(self, vertexId):
        del self.vs[vertexId]
        self.tabel.deleteRow(vertexId)

        for edge in (self.ed).values():
            numOfConnectedVertices = sum(self.tabel.getColumn(edge))
            if numOfConnectedVertices <= 1:
                self.deleteEdge(edge)
    
    def adjacent(self, vertex1, vertex2):
        v1Index = self.tabel.rows.index(vertex1)
        v2Index = self.tabel.rows.index(vertex2)

        for column in self.tabel.columns:
            edge = self.tabel.getColumn(column)
            if edge[v1Index] > 0 and edge[v2Index] > 0:
                return True
        return False

    def getNeighbors(self, vertexId):
        vertexIndex = self.tabel.rows.index(vertexId)
        neighbors = []
        for column in self.tabel.columns:
            edge = self.tabel.getColumn(column)
            if edge[vertexIndex] == 2:
                neighbors.append(self.getVertex(vertexIndex))
            elif edge[vertexIndex] == 1:
                edge[vertexIndex] = 0
                neighbors.append(self.getVertex(self.tabel.rows[edge.index(1)]))

        return neighbors

    def verticesForEdge(self, edgeId):
        verticesList = []
        collectionValues = self.tabel.getColumn(edgeId)
        vertices = self.tabel.rows

        con = zip(collectionValues,vertices)
        for pair in con:
            if pair[0] == 1:
                verticesList.append(self.getVertex(pair[1]))
            if pair[0] == 2:
                verticesList = [self.getVertex(pair[1]),self.getVertex(pair[1])]
        return verticesList

    def edgeWithAttribute(self, key, value):
        edges = []
        for edge in self.ed.values():
            try:
                if edge.attr[key] == value:
                    edges.append(edge)
            except:
                pass
        return edges

    def edgeWithColor(self, color):
        edges = []
        for edge in self.ed.values():
            if edge.color == color:
                edges.append(edge)
        return edges

    def verticesWithAttribute(self, key, value):
        vertices = []
        for vertex in self.ve.values():
            try:
                if vertex.attr[key] == value:
                    vertices.append(vertex)
            except:
                pass
        return vertices

    def verticesWithColor(self, color):
        vertices = []
        for vertex in self.ve.values():
            if vertex.color == color:
                vertices.append(vertex)
        return vertices

    def verticesWithLabel(self, label):
        vertices = []
        for vertex in self.ve.values():
            if vertex.label == str(label):
                vertices.append(vertex)
        return vertices

    def getVertexGrade(self,vertexId):
        row = self.tabel.getRow(vertexId)
        return sum(row)

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

def union(graphList):
    union = graphList[0]
    for i in range(1, len(graphList)):
        for vertex in graphList[i].ve.values():
            union.addVertex(vertex)
        for edge in graphList[i].ed.values():
            v1, v2 = graphList[i].getVertices(edge.id)
            union.addEdge(edge, v1.id, v2.id)
    return union