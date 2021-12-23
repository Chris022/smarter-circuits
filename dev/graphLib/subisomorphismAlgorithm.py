from graphLib.graph import Graph,Vertex,Edge,Table
import copy

def isValidIsomorphism(heystack,needle,matchingTable):
    needleVertexIds = matchingTable.rows
    for needlesVertexId in needleVertexIds:
        
        #get neighbours of needlesVertex
        needlesNeighbours = needle.getNeighborIds(needlesVertexId)
        
        #get the matching heystackVertex
        heystackVertexId = matchingTable.findInRow(needlesVertexId,1)

        #get the neighbours of the heystackVertex
        heystackNeighbours = heystack.getNeighborIds(heystackVertexId)

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
        for column in matchingTable.columns:
            if sum(matchingTable.getColumn(column)) == 1:
                matchList.append(heystack.getVertex(column))
        matchingsList.append(matchList)
    return matchingsList

def subisomorphism(heystack,needle):
    solutions = depthFirstSearch(heystack,needle)
    matches = convertMatchingTablesToList(heystack,solutions)
    return matches