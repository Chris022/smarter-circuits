import xml.etree.ElementTree as xml
#import igraph

from lib.graphLib.edge import Edge
from lib.graphLib.vertex import Vertex
from lib.graphLib.table import Table
import lib.graphLib.subisomorphismAlgorithm as algorithm


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
            self.table.addRow(vertex.id)
    
    def addEdge(self, edge, vertexId1, vertexId2):
        edge.__setId__(self.edIdCounter)
        self.edIdCounter +=1

        self.ed[edge.id] = edge
        self.table.addColumn(edge.id)
        #From
        self.table.addValue(vertexId1,edge.id)
        #To
        self.table.addValue(vertexId2,edge.id)

    def getVertices(self, edgeId):

        column = self.table.getColumn(edgeId)
        vertices = []
        for i in range(0, len(column)):
            if column[i] == 2:
                vertices.append(self.getVertex(self.table.rows[i]))
                vertices.append(self.getVertex(self.table.rows[i]))
            if column[i] == 1:
                vertices.append(self.getVertex(self.table.rows[i]))

        return vertices

    def deleteEdge(self, edgeId):
        del self.ed[edgeId]
        self.table.deleteColumn(edgeId)
    
    def deleteVertex(self, vertexId):
        del self.ve[vertexId]
        self.table.deleteRow(vertexId)

        clone = list((self.ed).values())
        for edge in clone:
            numOfConnectedVertices = sum(self.table.getColumn(edge.id))
            if numOfConnectedVertices <= 1:
                self.deleteEdge(edge.id)
    
    def adjacent(self, vertex1Id, vertex2Id):
        v1Index = self.table.rows.index(vertex1Id)
        v2Index = self.table.rows.index(vertex2Id)

        for column in self.table.columns:
            edge = self.table.getColumn(column)
            if edge[v1Index] > 0 and edge[v2Index] > 0:
                return True
        return False
    
    def getEdgeBetweenVertices(self,vertex1Id,vertex2Id):
        row1 = self.table.getRow(vertex1Id)
        row2 = self.table.getRow(vertex2Id)

        for i in range(0,len(row1)):
            if row1[i] == 1 and row2[i] == 1:
                return list(self.ed.values())[i]

    def getEdgesBetweenVertices(self,vertex1Id,vertex2Id):
        row1 = self.table.getRow(vertex1Id)
        row2 = self.table.getRow(vertex2Id)

        edges = []

        for i in range(0,len(row1)):
            if row1[i] == 1 and row2[i] == 1:
                edges.append(list(self.ed.values())[i])
        return edges

    def getNeighbors(self, vertexId):
        vertexIndex = self.table.rows.index(vertexId)
        neighbors = []
        for columnName in self.table.columns:
            column = self.table.getColumn(columnName)
            if column[vertexIndex] == 1:
                for index in range(0,len(column)):
                    if not index == vertexIndex:
                        if column[index] == 1:
                            neighbors.append(self.getVertex(self.table.rows[index]))
        return neighbors

    def getNeighborIds(self, vertexId):
        vertexIndex = self.table.rows.index(vertexId)
        neighbors = []
        for columnName in self.table.columns:
            column = self.table.getColumn(columnName)
            if column[vertexIndex] == 1:
                for index in range(0,len(column)):
                    if not index == vertexIndex:
                        if column[index] == 1:
                            neighbors.append(self.table.rows[index])  
        return neighbors

    def verticesForEdge(self, edgeId):
        verticesList = []
        collectionValues = self.table.getColumn(edgeId)
        vertices = self.table.rows

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
        row = self.table.getRow(vertexId)
        return sum(row)

    def getVerticesForEdge(self,edgeId):
        column = self.table.getColumn(edgeId)
        vertexIds = []
        for index in range(0,len(column)):
            if column[index] >= 1:
                vertexIds.append( list(self.ve.values())[index] )
        return vertexIds

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
            vertices = self.verticesForEdge(e.id)
            edge.attrib = {"source":"n"+str(vertices[0].id),"target":"n"+str(vertices[1].id)}

            data1 = xml.SubElement(edge,"data")
            data1.attrib = {"key":"e_color"}
            data1.text = str(e.color)

        xml_str = xml.tostring(xmlns, encoding='unicode')

        return '<?xml version="1.0" encoding="UTF-8"?>\n'+xml_str

    def group(self,vertices,replacementVertex):

        vertexIds = list(map(lambda x: x.id,vertices))
        
        #set of all vertices that have to be connected to the new replacementVertex
        edgeIds = set()
    
        #for every vertex that shall be replaced
        for vertexId in vertexIds:
            #get its neighbors
            neighborVertexIds = self.getNeighborIds(vertexId)
    
            #if the id is not part of the vertexids add it to the replacementVertexIds
            for neighborVertexId in neighborVertexIds:
                for edge in self.getEdgesBetweenVertices(vertexId, neighborVertexId):
                    edgeIds.add(edge.id)
                #if not neighborVertexId in vertexIds:
                #    replacementVertexNeighboursIds.add(neighborVertexId)
        
        #add new vertex
        self.addVertex(replacementVertex)

        #add all edges to the new Vertex
        for edgeId in edgeIds:
            vertices = self.getVerticesForEdge(edgeId)

            if vertices[0].id in vertexIds:
                self.addEdge(Edge(),vertices[1].id,replacementVertex.id)
            else:
                self.addEdge(Edge(),vertices[0].id,replacementVertex.id)

        #remove all vertexIds
        for vertexId in vertexIds:
            self.deleteVertex(vertexId)

    def insertVertex(self,vertex1Id,vertex2Id,insertionVertex):

        #get Edge between vertex1 and vertex2
        edge = self.getEdgeBetweenVertices(vertex1Id,vertex2Id)

        #delete Edge
        self.deleteEdge(edge.id)

        #add insertionVertex to graph
        self.addVertex(insertionVertex)

        #add edges
        self.addEdge(Edge(),vertex1Id,insertionVertex.id)
        self.addEdge(Edge(),insertionVertex.id,vertex2Id)

    def removeVertex(self,vertexId):
        #get neighbors of vertex
        neighborVertexIds  = self.getNeighborIds(vertexId)

        #create connection from every neighbor -> to every neighbor
        c = []
        for fromNei in neighborVertexIds:
            for toNei in neighborVertexIds:
                #if "to" and "from" are the same, don't connect them
                if fromNei == toNei: continue
                if set([fromNei,toNei]) in c: continue
                c.append(set([fromNei,toNei]))
                #connect "from" with "to"
                self.addEdge(Edge(),fromNei,toNei)

        #delte the vector that has to be removed
        self.deleteVertex(vertexId)

    def insertVertexByEdge(self,edgeId,insertionVertex):
        #get conneced Vertices for edge
        vertices = self.getVerticesForEdge(edgeId)

        #delete Edge
        self.deleteEdge(edgeId)

        #add insertionVertex to graph
        self.addVertex(insertionVertex)

        #add edges
        self.addEdge(Edge(),vertices[0].id,insertionVertex.id)
        self.addEdge(Edge(),insertionVertex.id,vertices[1].id)

    def getPatternMatches(self,pattern):
        mapings = algorithm.subisomorphism(self, pattern)

        mapings = list(map(lambda match: set(match), mapings))


        #remove duplicated
        final = []
        for i in mapings:
            if i not in final:
                final.append(i)
        return list(map(lambda f: list(f), final))

def union(graphList):
    union = graphList[0]
    for i in range(1, len(graphList)):
        for vertex in graphList[i].ve.values():
            union.addVertex(vertex)
        for edge in graphList[i].ed.values():
            v1, v2 = graphList[i].getVertices(edge.id)
            union.addEdge(edge, v1.id, v2.id)
    return union

