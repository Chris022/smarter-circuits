import re
import igraph as g
import math as m
import cv2
import json
import matplotlib.pyplot as plt
import itertools

from utils import getPixel,colorPixels,isOneColor,load1Pixel,drawRect
from constants import *


# Returns all Adjacent Pixels with a specific color
# image             -> 2D array with Pixel values
# pixel             -> coordinates of the pixel the others should be ajacent to
# color             -> the color of the "wanted" pixels
# blacklist         -> These pixels get ignored
def getAdjacentPixel(image,pixel,color,blacklist=[]):    
    adjacentPixels = [[-1,-1],[0,-1],[1,-1], \
                        [-1,0],        [1,0], \
                        [-1,1], [0,1], [1,1]]
    #create a array with the coordinates of all adjacentPixels
    validPixels = ([ pixel[0]+adj[0], pixel[1]+adj[1] ] for adj in adjacentPixels)
    #filter all pixels that are not the right color
    validPixels = list(
        filter(lambda coords: getPixel(image,coords) == color,validPixels)
    )
    #filter all pixels that are in the blacklist
    validPixels = list(
        filter(lambda x: not x in blacklist, validPixels)
    )

    return validPixels

# returns the coordinates of the first <color> pixel it finds
def findStaringPoint(image,color):
    for y in range(0,len(image)):
        for x in range(0,len(image[y])):
            if getPixel(image,x,y) == color:
                return [x,y]

# Runs along line until it finds the first Intersection
#
# image      -> The image
# startPoint -> Any random Point on the line
# color      -> The color of the Line
def findFirstIntersection(image,startPoint,color):

    def recursiveFindValidPoint(currentPixel,lastPixel,dir):
        adjacentPixels = getAdjacentPixel(image,currentPixel,color)
        if len(adjacentPixels) > 2:
            return currentPixel
        elif len(adjacentPixels) == 1:
            return recursiveFindValidPoint(adjacentPixels[dir],currentPixel,-1)
        else:
            adjacentPixels = getAdjacentPixel(image,currentPixel,color,[lastPixel]) 
            return recursiveFindValidPoint(adjacentPixels[dir],currentPixel,dir)
    return recursiveFindValidPoint(startPoint,None,0)

# Converts one connected Line into a Graph
# image -> binary image
# startingPoint -> tuple with the starting coords
# color -> the color of the foreground Pixels
def generatePartGraph(image,startPoint,color):
    #init recustion
    visitedCoords = []
    #count
    graph = g.Graph(directed=False)

    #add the starting Vector
    graph.add_vertex(str(startPoint), label=str(startPoint) ,color=INTERSECTION_COLOR,coordinate=tuple(startPoint))

    # recursive Function
    # currentCoord -> the coordinate of the current pixel
    # lastCoords -> the coordinates of the last visited pixels
    # lastVertexName -> name of the last added Vertex                                                           |------ knows only about verticies in this branch
    # dirGradient -> a list of all the directional steps the function took: 1->horizontal,0->vertical       ----|
    def recursiveGenerateGraph(currentCoord,lastCoords,lastVertexName,dirGradient):       #                     |------ knows only about verticies in this branch

        # start by creating an independent copy of the dirGradient list
        newDirGradient = list(dirGradient)

        #get the new directional Step
        # 1 = horizontal
        # 0 = vertical
        if(abs(currentCoord[0] - lastCoords[0]) < abs(currentCoord[1] - lastCoords[1])):
            newDirGradient.append(1)
        else:
            newDirGradient.append(0)

        # If the currentCoordinate has already been visited, this means a loop hast benn closed and you have to create a connection
        # from the last Vertex to this Vertex -> end recursion
        if currentCoord in visitedCoords:
            # check if the currentCoordinate has even a Vertex in the graph
            if len(graph.vs.select(name=str(currentCoord))):
                graph.add_edge(lastVertexName,str(currentCoord),color=EDGE_COLOR)
            return
        
        # add the current Cooridante to the visited Cooridantes
        visitedCoords.append(currentCoord)

        # get the adjacent Pixels to the current one
        adjacentPixels = getAdjacentPixel(image,currentCoord,color,[lastCoords])

        # if there are no more adjacent Pixels
        if len(adjacentPixels) == 0:
            #ENDPOINT

            # to prevent self Loop
            if(str(currentCoord) != lastVertexName):
                graph.add_vertex(str(currentCoord),label=str(currentCoord),color=END_COLOR,coordinate=tuple(currentCoord))
                # connect lastVertexId to the just added Vertex

                graph.add_edge(lastVertexName,str(currentCoord),color=EDGE_COLOR)
        
        #if there is exactly one adjacent Pixel
        elif len(adjacentPixels) == 1:
            #LINE

            # check if the dir Gradent is longer then 6 -> otherwhise ignore dir changes and recursive call
            if len(newDirGradient) > 6:

                # calculate the current dir by taking the last 4 elements and avaraging them
                currDire = sum(newDirGradient[-4:])/4 < 0.5
                # calcualte the newDirGradient dir by taking the 4 elements form the 5 least to the second least and avaraging them
                lastDire = sum(newDirGradient[-5:-1])/4 < 0.5
                # if the direction changed add a new corner vertex else just recursive call the function
                if not  currDire == lastDire:
                    # to prevent self Loop
                    graph.add_vertex(str(currentCoord),label=str(currentCoord),color=CORNER_COLOR,coordinate=tuple(currentCoord))
                    graph.add_edge(lastVertexName,str(currentCoord),color=EDGE_COLOR)
                    recursiveGenerateGraph(adjacentPixels[0],currentCoord,str(currentCoord),newDirGradient)
                else:
                    recursiveGenerateGraph(adjacentPixels[0],currentCoord,lastVertexName,newDirGradient)
            else:
                recursiveGenerateGraph(adjacentPixels[0],currentCoord,lastVertexName,newDirGradient)

        else:
            #INTERSECTION

            # to prevent self Loop
            if(str(currentCoord) != lastVertexName):
                # to prevent self Loop
                graph.add_vertex(str(currentCoord),label=str(currentCoord),color=INTERSECTION_COLOR,coordinate=tuple(currentCoord))
                graph.add_edge(lastVertexName,str(currentCoord),color=EDGE_COLOR)
            #for every line going out of the intersection recursive call
            for adjacentPixel in adjacentPixels:
                recursiveGenerateGraph(adjacentPixel,currentCoord,str(currentCoord),[])
            
    recursiveGenerateGraph(startPoint,[0,0],str(startPoint),[])
    return graph,visitedCoords


def generateWholeGraph(image,foregroundColor,backgroundColor):
    graphCollection = []
    while True:
        startingPoint = findStaringPoint(image,foregroundColor)
        if(startingPoint):
            startingPoint = findFirstIntersection(image,startingPoint,foregroundColor)
            G,visitedPixels = generatePartGraph(image,startingPoint,foregroundColor)
            graphCollection.append(G)
            #Remove all visited Pixels
            image = colorPixels(image,visitedPixels,backgroundColor)
            if isOneColor(image,backgroundColor):
                print("end reached")
                break
        else:
            print("stoped before end")
            break

    return g.union(graphCollection)

#Returns a List of all the Node Colors in a Graph
def getColorListNode(graph):
    colorList = []
    for vert in graph.vs:
        if vert["color"] == INTERSECTION_COLOR:
            colorList.append(0)
        elif vert["color"] == END_COLOR:
            colorList.append(1)
        elif vert["color"] == CORNER_COLOR:
            colorList.append(2)
        elif vert["color"] == OTHER_NODE_COLOR:
            colorList.append(3)
    return colorList

#Returns a List of all the Edge Colors in a Graph
def getColorListEdge(graph):
    colorList = []
    for edge in graph.es:
        try:
            if edge["color"] == OTHER_EDGE_COLOR:
                colorList.append(1)
            else:
                colorList.append(0)
        except:
            colorList.append(0)
    return colorList

#Retuns a node by name
def getNode(graph,name):
    graph

#Takes a Graph and a Pattern and returns a list of lists of mathching coordinates
# [[PatternMatches],[OtherPatternMatch]]
# If sort = True -> All the Coordinates in a Match get Sorted
# Double Matches are remove
def getPatternMatches(graph,pattern):
    mapings = graph.get_subisomorphisms_vf2(pattern,color1=getColorListNode(graph),color2=getColorListNode(pattern),edge_color1=getColorListEdge(graph),edge_color2=getColorListEdge(pattern))
    result = []
    for i in range(0,len(mapings)):
        # Get all the coordinates of the Notes that match the pattern
        result.append(list( map(lambda node:json.loads(graph.vs.find(node)["label"]) ,mapings[i]) ))

    #result is a 2D array [List of Matched Patterns] [[List of Coordinates that match]]
    #Sort the List of Coorinates that match, in order to remove doubles
    for i in range(0,len(result)):
        result[i] = list(sorted(result[i]))
    #remove duplicated
    final = []
    for i in result:
        if i not in final:
            final.append(i)
    return final


# Takes a Graph
# Searches the Graph for Grounds
# checks if the "center" of a Ground is close to the "center" of another
# It then checks if there is more than one other Note between the two Intersections (To avoid the connection of 2 close tougheter Caps)
# if they are, the two Intersections are replaced with Other-Notes
# and they get connected by a Other Line
# returns: the modified Graph
def connectCapsTougehter(graph):
    ground = g.Graph(directed=False)
    ground.add_vertex(0,color=END_COLOR)
    ground.add_vertex(1,color=INTERSECTION_COLOR)
    ground.add_vertex(2,color=END_COLOR)
    ground.add_edge(1,0)
    ground.add_edge(1,2)

    # Match all ground Symbols
    groundMatches = getPatternMatches(graph,ground)

    #now calculate the distance between each and every ground
    #create parinings (permutations without order) example: [1,2,3] -> [1,2],[2,3],[1,3]
    combintations = list(itertools.combinations(groundMatches,2))
    #for every combination
    for combination in combintations:
        #check distance between two red nodes of the Ground symbol      (End)--(Center/Intersection)--(End)

        #get Intersection node in every combination
        redOne = list(filter(lambda x: graph.vs.select(name=str(x))['color'][0] == INTERSECTION_COLOR,combination[0]))
        redTwo = list(filter(lambda x: graph.vs.select(name=str(x))['color'][0] == INTERSECTION_COLOR,combination[1]))
        if len(redOne)== 1 and len(redTwo) == 1 and redOne != redTwo:
            redOne = redOne[0]
            redTwo = redTwo[0]
            #check distance between the two
            if m.sqrt((redOne[0] - redTwo[0])**2 + (redOne[1] - redTwo[1])**2)  < 25:
                #only if the two are not directly connected
                numberOfNodesBetween = graph.shortest_paths_dijkstra(source=str(redOne), target = str(redTwo), mode="all")[0][0]
                if not numberOfNodesBetween == 1:
                    graph.vs.select(name=str(redOne))['color'] = OTHER_NODE_COLOR
                    graph.vs.select(name=str(redTwo))['color'] = OTHER_NODE_COLOR
                    graph.add_edge(str(redOne),str(redTwo),color=OTHER_EDGE_COLOR)
    return graph

# Ground Graph Patterns
def groundPattern():
    ground = g.Graph(directed=False)
    ground.add_vertex(0,color=END_COLOR)
    ground.add_vertex(1,color=INTERSECTION_COLOR)
    ground.add_vertex(2,color=END_COLOR)
    ground.add_edge(1,0)
    ground.add_edge(1,2)
    return ground

# Cap Graph Pattern
def capPattern():
    cap = g.Graph(directed=False)
    cap.add_vertex(0,color=END_COLOR)
    cap.add_vertex(1,color=OTHER_NODE_COLOR)
    cap.add_vertex(2,color=END_COLOR)
    cap.add_edge(1,0)
    cap.add_edge(1,2)

    cap.add_vertex(3,color=END_COLOR)
    cap.add_vertex(4,color=OTHER_NODE_COLOR)
    cap.add_vertex(5,color=END_COLOR)
    cap.add_edge(4,3)
    cap.add_edge(4,5)

    cap.add_edge(1,4, color=OTHER_EDGE_COLOR)
    return cap

# Resistor Graph Pattern
def resistorPattern():
    res = g.Graph(directed=False)
    res.add_vertex(0,color=INTERSECTION_COLOR)
    res.add_vertex(1,color=CORNER_COLOR)
    res.add_vertex(2,color=CORNER_COLOR)
    res.add_vertex(3,color=INTERSECTION_COLOR)
    res.add_vertex(4,color=CORNER_COLOR)
    res.add_vertex(5,color=CORNER_COLOR)
    res.add_edge(0,1)
    res.add_edge(1,2)
    res.add_edge(2,3)
    res.add_edge(3,4)
    res.add_edge(4,5)
    res.add_edge(5,0)
    return res

# Takse a List of coordinates returns the coordinates of the upper left and lower right corner
def generateBoundingBox(listOfCoords,offset):
    xCoords = list(map(lambda x: x[0],listOfCoords))
    yCoords = list(map(lambda y: y[1],listOfCoords))

    #get smalles and biggest of each and create Box
    from_ = [min(xCoords)-offset,min(yCoords)-offset]
    to_ = [max(xCoords)+offset,max(yCoords)+offset]
    return [from_,to_]

# 
def generateBoudingBoxes(image):
    # Generate the Graph without the Cap connections
    union = generateWholeGraph(image,FOREGROUND,BACKGROUND)
    # Connect Caps
    union = connectCapsTougehter(union)

    
    patterns =  [    capPattern(), \
                    resistorPattern(), \
                    groundPattern(), \
                ]
    matches = (getPatternMatches(union, pattern) for pattern in patterns)
    matches = sum(matches,[]) # Flattens a List of List
    boundingBoxes = list(map(lambda x: generateBoundingBox(x,5),matches))
    return boundingBoxes


#imageArray = load1Pixel("./../src/testImages","2.png",binary=True)
#colorImage = load1Pixel("./../src/testImages","2.png",color=True)
#
#boundingBoxes = generateBoudingBoxes(imageArray)
#print(len(boundingBoxes))
#for boundingBox in boundingBoxes:
#    drawRect(colorImage,boundingBox,(255,0,0))
#colorImage = cv2.cvtColor(255-colorImage, cv2.COLOR_BGR2RGB)
#plt.imshow(colorImage,interpolation="bilinear")
#plt.waitforbuttonpress(0)