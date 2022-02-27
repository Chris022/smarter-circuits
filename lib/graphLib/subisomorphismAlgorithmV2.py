from copy import deepcopy

from lib.graphLib.table import Table
import numpy as np

#checkes of a vertex I in needle can be mapped to a vertex J in heystack
#does this by checking:
#   color(I) = color(J)
#   degree(I) <= degree(J)
def checkMapping(needle,I,heystack,J):
    #color
    colorI = I.color
    colorJ = J.color
    if(colorI != colorJ):
        return False
    
    #degree
    degreeI = len(needle.getNeighborIds(I.id))
    degreeJ = len(heystack.getNeighborIds(J.id))
    if(degreeI > degreeJ):
        return False

    return True

#used to remove impossible mappings
#get all neighbors x of every heystack vertex
#get all neighbors y of the neighbor of the needle vertex
#only if all y are also neighbors of x the mapping is possible
def simplify(heystack,needle,matrix):

    #as long as the matrix still was changed!
    matrixWasSimplified = True
    while matrixWasSimplified:
        matrixWasSimplified = False
        #for all Values in the matrix
        for j in range(0,len(heystack.ve)):
            x = list((heystack.ve).values())[j]
            for i in range(0,len(needle.ve)):
                y = list((needle.ve).values())[i]

                if matrix[i,j] == 0:
                    continue

                #get the neighbors of x
                heystackNeighbors = heystack.getNeighbors(x.id)
                #get all neighbors of y
                needleNeighbors = needle.getNeighbors(y.id)

                #for all neighbors of the heystack
                for needleNeighbor in needleNeighbors:
                    isThereOne = False
                    #for all neighbors of the needle
                    for heystackNeighbor in heystackNeighbors:
                        #get the indices of the heystack- and needle-Neighbors
                        hesytackIndex = list(heystack.ve.values()).index(heystackNeighbor)
                        needleIndex = list(needle.ve.values()).index(needleNeighbor)

                        if matrix[needleIndex,hesytackIndex] == 1:
                            isThereOne = True

                    if not isThereOne:
                        matrix[i,j] = 0
                        matrixWasSimplified = True

    return matrix


def checkIsIsomorphism(heystack,needle,mapping):

    M = np.matrix(mapping)

    #get all adjacency matrixes
    H = np.matrix(heystack.getAdjacencyMatrix().values)
    N = np.matrix(needle.getAdjacencyMatrix().values)

    #M*(M*H)T == N wenn isomorphism
    newN = M*((M*H).getT())

    #TODO: Check colors!

    return N.tolist() == newN.tolist()


def outerRecurse(heystack,needle,matrix):
    possibleMappings = []
    # recursive function for generation all mappings
    def recurse(used_columns,cur_row,heystack,needle,matrix):

        if cur_row == len(matrix):

            #check if matrix is a isomorphism:
            if checkIsIsomorphism(heystack,needle,matrix):
                print(matrix)
                print("--------------------------")
                possibleMappings.append(matrix)
                #output yes and end the algorithm
                return matrix

            return None

        #simplify
        matrix = simplify(heystack,needle,matrix)

        for column in range(0,len(matrix[0])):
            if column in used_columns:
                continue

            #if the current column in the current row is 0 -> skip!
            if matrix[cur_row,column] == 0:
                continue
            
            #create immutalbe copy of matrix
            matrix_ = deepcopy(matrix)

            #set all columns in the current row to 0 exept the current column
            matrix_[cur_row,:] = 0
            matrix_[cur_row,column] = 1

            #mark the current column as used
            used_columns_ = list(used_columns)
            used_columns_.append(column)
            recurse(used_columns_,cur_row+1,heystack,needle,matrix_)

        return False
    recurse([],0,heystack,needle,matrix)
    return possibleMappings

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

def ulmansSubgraph(heystack,needle):

    # Start by createing a |needle|x|heystack| matrix
    dimensions = (len(needle.ve),len(heystack.ve))
    matrix = np.zeros(dimensions,dtype=int)

    # Set all Elements to 1 if mapping from needle Vertex to heystack Vertex is possible
    for j in range(0,len(heystack.ve)):
        J = list((heystack.ve).values())[j]
        for i in range(0,len(needle.ve)):
            I = list((needle.ve).values())[i]
            mapping = checkMapping(needle,I,heystack,J)
            if mapping:
                matrix[i,j] = 1
    
    matches = outerRecurse(heystack,needle,matrix)
    #convert the returned matches back to tables
    heystackVertices = list(map(lambda v:v.id,heystack.ve.values()))
    needleVertices = list(map(lambda v:v.id,needle.ve.values()))
    matchingTables = [Table.withColumnsAndRowsAndValues(needleVertices,heystackVertices,match) for match in matches]
    return convertMatchingTablesToList(heystack,matchingTables)





