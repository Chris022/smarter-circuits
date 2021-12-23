from graph import Graph,Vertex,Edge,Table
import copy

# Constructing Graph
bigGraph = Graph()
v1 = Vertex()
v2 = Vertex()
v3 = Vertex()
v4 = Vertex()
v5 = Vertex()
e1 = Edge()
e2 = Edge()
e3 = Edge()
e4 = Edge()
e5 = Edge()

bigGraph.addVertex(v1)
bigGraph.addVertex(v2)
bigGraph.addVertex(v3)
bigGraph.addVertex(v4)
bigGraph.addVertex(v5)
bigGraph.addEdge(e1, v1.id, v2.id)
bigGraph.addEdge(e2, v2.id, v3.id)
bigGraph.addEdge(e3, v3.id, v4.id)
bigGraph.addEdge(e4, v4.id, v1.id)
bigGraph.addEdge(e5, v3.id, v5.id)

searchGraph = Graph()
v6 = Vertex()
v7 = Vertex()
v8 = Vertex()
v9 = Vertex()
e6 = Edge()
e7 = Edge()
e8 = Edge()
e9 = Edge()
searchGraph.addVertex(v6)
searchGraph.addVertex(v7)
searchGraph.addVertex(v8)
searchGraph.addVertex(v9)
searchGraph.addEdge(e6, v6.id, v7.id)
searchGraph.addEdge(e7, v7.id, v8.id)
searchGraph.addEdge(e8, v8.id, v9.id)
searchGraph.addEdge(e9, v9.id, v6.id)

def isValidIsomorphism(heystack,needle,matchingTable):
    needleVertexIds = matchingTable.rows
    for needlesVertexId in needleVertexIds:
        
        #get neighbours of needlesVertex
        needlesNeighbours = needle.getNeighbors(needlesVertexId)
        
        #get the matching heystackVertex
        heystackVertexId = matchingTable.findInRow(needlesVertexId,1)

        #get the neighbours of the heystackVertex
        heystackNeighbours = heystack.getNeighbors(heystackVertexId)

        #for every needleNeighbour check if it matches with a heystackNeighbour
        for needleNeighbour in needlesNeighbours:
            connectedHeystack = matchingTable.findInRow(needleNeighbour,1)
            if not connectedHeystack in heystackNeighbours:
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
        
        # now get all needle vertices with higher or equal grade and same color
        for needleVertexId in needleVertexIds:
            needleGrade = needle.getVertexGrade(needleVertexId)
            if heystackGrade >= needleGrade:
                matchingTable.setValue(
                    needleVertexId,
                    heystackVertexId,
                    1
                )
    return matchingTable


def depthFirstSearch(heystack,needle):
    matches = []
    matchingTable = generateMatchingTable(heystack,needle)
    def recursive(currentRow,usedColumns,matchingTable):

        #Create independant copies of arguments
        usedColumns = list(usedColumns)
        matchingTable = copy.deepcopy(matchingTable)

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
                #set the column to be used
                usedColumns.append(columnName)
                #set the whole row to 0 accept the used column
                newTable = copy.deepcopy(matchingTable)
                newTable.changeRowByIndex(currentRow,lambda val,column: val if column == columnName else 0)
                #
                recursive(currentRow+1,usedColumns,newTable)
                #unset column
                usedColumns.remove(columnName)
    recursive(0,[],matchingTable)
    return matches

def convertMatchingTablesToList(heystack,matchingTables):
    matchingsList = []
    #for every Table
    for matchingTable in matchingTables:
        matchList = []
        #get all rows with a 1
        for row in matchingTable.rows:
            if sum(matchingTable.getRow(row)) == 1:
                matchList.append(heystack.getVertex(row))
        matchingsList.append(matchList)
    return matchingsList
    
solutions = depthFirstSearch(bigGraph,searchGraph)
matches = convertMatchingTablesToList(bigGraph,solutions)
print(matches)