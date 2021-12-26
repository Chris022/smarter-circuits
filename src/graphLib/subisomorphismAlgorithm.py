from graph import Graph,Vertex,Edge,Table
import copy
import time

#create Graph
heystack = Graph()

v0 = Vertex("blue")
v1 = Vertex("red")
v2 = Vertex("blue")
v3 = Vertex("red")
v4 = Vertex("red")
v5 = Vertex("red")
v6 = Vertex("blue")
v7 = Vertex("blue")
v8 = Vertex("red")
v9 = Vertex("yellow")
v10 = Vertex("yellow")
v11 = Vertex("red")
v12 = Vertex("yellow")
v13 = Vertex("yellow")
v14 = Vertex("red")
v15 = Vertex("red")
v16 = Vertex("blue")
v17 = Vertex("blue")
v18 = Vertex("red")
v19 = Vertex("blue")
v20 = Vertex("red")
v21 = Vertex("blue")
heystack.addVertices([v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21])
heystack.addEdge(Edge(),v0.id,v1.id)
heystack.addEdge(Edge(),v1.id,v2.id)
heystack.addEdge(Edge(),v1.id,v3.id)
heystack.addEdge(Edge(),v3.id,v4.id)
heystack.addEdge(Edge(),v4.id,v5.id)
heystack.addEdge(Edge(),v5.id,v6.id)
heystack.addEdge(Edge(),v5.id,v7.id)
heystack.addEdge(Edge(),v4.id,v8.id)
heystack.addEdge(Edge(),v8.id,v9.id)
heystack.addEdge(Edge(),v9.id,v10.id)
heystack.addEdge(Edge(),v10.id,v11.id)
heystack.addEdge(Edge(),v11.id,v12.id)
heystack.addEdge(Edge(),v12.id,v13.id)
heystack.addEdge(Edge(),v13.id,v8.id)
heystack.addEdge(Edge(),v11.id,v14.id)
heystack.addEdge(Edge(),v14.id,v15.id)
heystack.addEdge(Edge(),v15.id,v16.id)
heystack.addEdge(Edge(),v15.id,v17.id)
heystack.addEdge(Edge(),v14.id,v18.id)
heystack.addEdge(Edge(),v18.id,v13.id)
heystack.addEdge(Edge(),v18.id,v20.id)
heystack.addEdge(Edge(),v20.id,v19.id)
heystack.addEdge(Edge(),v20.id,v21.id)


needle = Graph()
v22 = Vertex("blue")
v23 = Vertex("red")
v24 = Vertex("blue")
needle.addVertex(v22)
needle.addVertex(v23)
needle.addVertex(v24)
needle.addEdge(Edge(),v22.id,v23.id)
needle.addEdge(Edge(),v23.id,v24.id)
needle = Graph()
v1 = Vertex(color="red")
v2 = Vertex(color="yellow")
v3 = Vertex(color="yellow")
v4 = Vertex(color="red")
v5 = Vertex(color="yellow")
v6 = Vertex(color="yellow")
needle.addVertices([v1,v2,v3,v4,v5,v6])
needle.addEdge(Edge(), v1.id, v2.id)
needle.addEdge(Edge(), v2.id, v3.id)
needle.addEdge(Edge(), v3.id, v4.id)
needle.addEdge(Edge(), v4.id, v5.id)
needle.addEdge(Edge(), v5.id, v6.id)
needle.addEdge(Edge(), v6.id, v1.id)


def isValidIsomorphism(heystack,needle,matchingTable):
    needleVertexIds = matchingTable.rows
    for needlesVertexId in needleVertexIds:
        
        #get neighbours of needlesVertex
        needlesNeighbours = needle.getNeighborIds(needlesVertexId)
        
        #get the matching heystackVertex
        heystackVertexId = matchingTable.findInRow(needlesVertexId,1)

        #get the neighbours of the heystackVertex
        heystackNeighbors = heystack.getNeighborIds(heystackVertexId)

        #get the colors of all edges between the needle and the needleNeighbors
        needleEdgeColors = [] #TODO

        #for every needleNeighbour check if it matches with a heystackNeighbour
        for needleNeighbour in needlesNeighbours:
            connectedHeystack = matchingTable.findInRow(needleNeighbour,1)
            #get the color of the edge between the connectedHeystack and the Heystack
            heystackColor = None #TODO
            if not connectedHeystack in heystackNeighbors and heystackColor in needleEdgeColors:
                return False
    return True

# two vertexes only match if the g rade of the second one is higher than the one of the first one
# (and if their colors usw. match)
def generateMatchingTable(heystack,needle):
    
    heystackVertexIds   = list(heystack.ve.keys())
    needleVertexIds     = list(needle.ve.keys())

    matchingTable = Table.withColumnsAndRows(
                        rows=needleVertexIds,
                        columns=heystackVertexIds
                    )
    
    #for every Row (heystackVertex)
    for heystackVertexId in heystackVertexIds:
        # get grade (and color)
        heystackGrade = heystack.getVertexGrade(heystackVertexId)
        heystackColor = heystack.getVertex(heystackVertexId).color
        
        # now get all needle vertices with higher or equal grade and same color
        for needleVertexId in needleVertexIds:
            needleGrade = needle.getVertexGrade(needleVertexId)
            needleColor = needle.getVertex(needleVertexId).color
            if heystackGrade >= needleGrade and needleColor == heystackColor:
                matchingTable.setValue(
                    needleVertexId,
                    heystackVertexId,
                    1
                )
    return matchingTable

def simplify(heystack,needle,matchingTable):

    somethingChanged = True
    while somethingChanged:
        somethingChanged = False
        # for every 1 in the Table
        for y in matchingTable.rows:
            for x in matchingTable.columns:
                if matchingTable.getValue(y,x) == 1:

                    needleNeighbors = needle.getNeighborIds(y)
                    heystackNeighbors = heystack.getNeighborIds(x)

                    for needleNeighbor in needleNeighbors:
                        isThereOne = False
                        for heystackNeighbor in heystackNeighbors:

                            if matchingTable.getValue(needleNeighbor,heystackNeighbor) == 1:
                                isThereOne = True
                        if not isThereOne:
                            matchingTable.setValue(y,x,0)
                            somethingChanged = True
    return matchingTable


def depthFirstSearch(heystack,needle,matchingTable):
    matches = []
    def recursive(currentRow,usedColumns,matchingTable):

        #Create independant copies of arguments
        usedColumns = list(usedColumns)
        matchingTable = copy.deepcopy(matchingTable)
        matchingTable = simplify(heystack,needle,matchingTable)

        #End Condition
        # If the last Row
        if currentRow == len(matchingTable.rows):
            # check if every row has only one 1
            every = True
            for row in matchingTable.values:
                if not sum(row) == 1:
                    every = False
            #check if it is a valid Isomorphism
            if every and isValidIsomorphism(heystack,needle,matchingTable):
                matches.append(matchingTable)
            return

        #For every unused Column
        for columnName in matchingTable.columns:
            if not columnName in usedColumns:
                if not matchingTable.getValue(matchingTable.rows[currentRow],columnName) == 1:
                    continue
                #set the column to be used
                usedColumns.append(columnName)
                #set the whole row to 0 accept the used column
                newTable = copy.deepcopy(matchingTable)
                newTable.changeRowByIndex(currentRow,lambda val,column: val if column == columnName else 0)
                #
                recursive(currentRow+1,usedColumns,newTable)
                #unset column
                usedColumns.remove(columnName)
        return
    recursive(0,[],matchingTable)
    return matches




def convertMatchingTablesToList(heystack,matchingTables):
    matchingsList = []
    #for every Table
    for matchingTable in matchingTables:
        matchList = []
        #get all rows with a 1
        for column in matchingTable.columns:
            if sum(matchingTable.getColumn(column)) == 1:
                matchList.append(heystack.getVertex(column))
        matchingsList.append(matchList)
    return matchingsList

def subisomorphism(heystack,needle): 
    matchingTable = generateMatchingTable(heystack,needle)
    solutions = depthFirstSearch(heystack,needle,matchingTable)
    matches = convertMatchingTablesToList(heystack,solutions)
    return matches