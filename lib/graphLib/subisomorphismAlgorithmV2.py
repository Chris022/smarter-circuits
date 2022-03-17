from copy import deepcopy
from itertools import product
import numpy as np

from lib.graphLib.table import Table

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

#Taks a mapping and a heystack graph
#Removes all vertices from the heystack graph, that are not mapped to anything
#So that in the end, only the mapped Graph is left
def heystackGraphToMappedGraph(mapping,heystack):

    #remove all vertices from the heystack, that are not mapped to anything!
    heystack_copy = deepcopy(heystack)
    heystack_copy_vertices = list(heystack_copy.ve.values())
    for j in range(0,len(heystack_copy_vertices)):
        if sum(mapping[:,j]) == 0: # if there is no 1 in the row in the mapping (the vertex is not used in the mapping)
            not_used_vertex = heystack_copy_vertices[j]
            heystack_copy.deleteVertex(not_used_vertex.id)

    return heystack_copy

#used to remove impossible mappings
#get all neighbors x of every heystack vertex
#get all neighbors y of the neighbor of the needle vertex
#only if all y are also neighbors of x the mapping is possible
def simplify(heystack,heystack_adj_matrix,needle,needle_adj_matrix,matrix):

    heystack_vertices= list(heystack.ve.values())
    heystack_indices = list(range(0,len(heystack_vertices)))
    
    needle_vertex = list(needle.ve.values())
    needle_indices = list(range(0,len(needle_vertex)))

    #as long as the matrix still was changed!
    matrixWasSimplified = True
    while matrixWasSimplified:
        matrixWasSimplified = False
        #for all Values in the matrix
        pairs = list(product(heystack_indices,needle_indices))
        for (j,i) in pairs:

            if matrix[i,j] == 0:
                continue

            x = heystack_vertices[j]
            y = needle_vertex[i]

            #get the neighbors of x
            heystackNeighbors = heystack.getNeighborsWithAdjacencyMatrix(heystack_adj_matrix,x.id)
            #get all neighbors of y
            needleNeighbors =  needle.getNeighborsWithAdjacencyMatrix(needle_adj_matrix,y.id)

            #for all neighbors of the heystack
            for needleNeighbor in needleNeighbors:
                isThereOne = False
                #for all neighbors of the needle
                for heystackNeighbor in heystackNeighbors:
                    #get the indices of the heystack- and needle-Neighbors
                    hesytackIndex = heystack_vertices.index(heystackNeighbor)
                    needleIndex = needle_vertex.index(needleNeighbor)

                    if matrix[needleIndex,hesytackIndex] == 1:
                        isThereOne = True

                if not isThereOne:
                    matrix[i,j] = 0
                    matrixWasSimplified = True              

    return matrix


def checkIsIsomorphism(heystack,heystack_adj_matrix,needle,needle_adj_matrix,mapping):

    M = np.matrix(mapping)

    #get all adjacency matrixes
    H = np.matrix(heystack_adj_matrix.values)
    N = np.matrix(needle_adj_matrix.values)

    #M*(M*H)T == N wenn isomorphism
    newN = M*((M*H).getT())

    is_valid = N.tolist() == newN.tolist()

    if not is_valid:
        return False

    #TODO: IMPROVE COLOR CHECKING
    #get all colors in needle
    needle_edge_colors = list(map(lambda x: x.color,needle.ed.values()))
    needle_vertex_colors = list(map(lambda x: x.color,needle.ve.values()))
    
    #get all colors in mapped heystack
    mapped_heystack_vertex = heystackGraphToMappedGraph(mapping,heystack)
    heystack_edge_colors = list(map(lambda x: x.color,mapped_heystack_vertex.ed.values()))
    heystack_vertex_colors = list(map(lambda x: x.color,mapped_heystack_vertex.ve.values()))

    #check if vertex_colors are the same
    is_valid = is_valid and sorted(needle_vertex_colors) == sorted(heystack_vertex_colors)
    #check if edges_colors  are the same
    is_valid = is_valid and sorted(needle_edge_colors) == sorted(heystack_edge_colors)

    return is_valid


def outerRecurse(heystack,needle,matrix):
    possibleMappings = []
    heystack_adj_matrix = heystack.getAdjacencyMatrix()
    needle_adj_matrix   = needle.getAdjacencyMatrix()
    # recursive function for generation all mappings
    def recurse(used_columns,cur_row,heystack,needle,matrix):

        if cur_row == len(matrix):

            #check if matrix is a isomorphism:
            if checkIsIsomorphism(heystack,heystack_adj_matrix,needle,needle_adj_matrix,matrix):
                possibleMappings.append(matrix)
                #output yes and end the algorithm
                return matrix

            return None

        #simplify
        matrix = simplify(heystack,heystack_adj_matrix,needle,needle_adj_matrix,matrix)
        #if delta_time:
        #    print(delta_time)

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





