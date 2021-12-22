import xml.etree.ElementTree as xml
#import igraph

from graphLib.edge import Edge
from graphLib.vertex import Vertex
from graphLib.incidenceMatrix import IncidenceMatrix


class Graph:

    def __init__(self) -> None:
        self.veIdCounter = 0
        self.ve = {}   # type_: {id:Vertex}
        self.edIdCounter = 0
        self.ed = {}   # type_: {id:Edge}
        self.incidenceMatrix = IncidenceMatrix()

    def getVertex(self, vertexId):
        return self.ve[vertexId]

    def getEdge(self, edgeId):
        return self.ed[edgeId]

    def addVertex(self, vertex):
        vertex.__setId__(self.veIdCounter)
        self.veIdCounter +=1

        self.ve[vertex.id] = vertex
        self.incidenceMatrix.addRow(vertex.id)

    def addVertecies(self, vertecies):
        for vertex in vertecies:
            vertex.__setId__(self.veIdCounter)
            self.veIdCounter +=1

            self.ve[vertex.id] = vertex
            self.incidenceMatrix.addRow(vertex.id)
    
    def addEdge(self, edge, vertexId1, vertexId2):
        edge.__setId__(self.edIdCounter)
        self.edIdCounter +=1

        self.ed[edge.id] = edge
        self.incidenceMatrix.addColumn(edge.id)
        #From
        self.incidenceMatrix.addValue(vertexId1,edge.id)
        #To
        self.incidenceMatrix.addValue(vertexId2,edge.id)

    def getVertecies(self, edgeId):

        column = self.incidenceMatrix.getColumn(edgeId)
        vertecies = []
        for i in range(0, len(column)):
            if column[i] == 2:
                vertecies.append(self.getVertex(self.incidenceMatrix.rows[i]))
                vertecies.append(self.getVertex(self.incidenceMatrix.rows[i]))
            if column[i] == 1:
                vertecies.append(self.getVertex(self.incidenceMatrix.rows[i]))

        return vertecies

    def deleteEdge(self, edgeId):
        del self.ed[edgeId]
        self.incidenceMatrix.deleteColumn(edgeId)
    
    def deleteVertex(self, vertexId):
        del self.vs[vertexId]
        self.incidenceMatrix.deleteRow(vertexId)

        for edge in (self.ed).values():
            numOfConnectedVertices = sum(self.incidenceMatrix.getColumn(edge))
            if numOfConnectedVertices <= 1:
                self.deleteEdge(edge)
    
    def adjacent(self, vertexId1, vertexId2):
        v1Index = self.incidenceMatrix.rows.index(vertexId1)
        v2Index = self.incidenceMatrix.rows.index(vertexId2)

        for column in self.incidenceMatrix.columns:
            edge = self.incidenceMatrix.getColumn(column)
            if edge[v1Index] > 0 and edge[v2Index] > 0:
                return True
        return False

    def getNeighbors(self, vertexId):
        vertexIndex = self.incidenceMatrix.rows.index(vertexId)
        neighbors = []
        for column in self.incidenceMatrix.columns:
            edge = self.incidenceMatrix.getColumn(column)
            if edge[vertexIndex] == 2:
                neighbors.append(self.getVertex(vertexIndex))
            elif edge[vertexIndex] == 1:
                edge[vertexIndex] = 0
                neighbors.append(self.getVertex(self.incidenceMatrix.rows[edge.index(1)]))

        return neighbors

    def verticesForEdge(self, edgeId):
        verticesList = []
        collectionValues = self.incidenceMatrix.getColumn(edgeId)
        vertices = self.incidenceMatrix.rows

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
            vertecies = self.verticesForEdge(e.id)
            edge.attrib = {"source":"n"+str(vertecies[0].id),"target":"n"+str(vertecies[1].id)}

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
            v1, v2 = graphList[i].getVertecies(edge.id)
            union.addEdge(edge, v1.id, v2.id)
    return union