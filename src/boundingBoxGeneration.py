import copy
def generateBoundingBox(verticesList,image):
    image = copy.deepcopy(image)

    #start by generating a boundingbox simply by using the verticesList
    listOfCoords = list(map(lambda x: x.attr['coordinates'],verticesList))

    xCoords = list(map(lambda x: x[0],listOfCoords))
    yCoords = list(map(lambda y: y[1],listOfCoords))

    #get smalles and biggest of each and create Box
    from_ = [min(xCoords)-7,min(yCoords)-7]
    to_ = [max(xCoords)+7,max(yCoords)+7]

    #Problem: Sometimes a component dosen't have an vertex at its furthest component (round components!)
    #Solution: Increace the Size of the Bondingbox until there are only X lines passing through it!

    addXRight = 0
    addXLeft = 0
    while True:
        #counts how often the Bounding box passes through a line
        passesLeft = 0
        passesRight = 0
        for y in range(from_[1],to_[1]):
            try:
                if image[y][from_[0]-addXLeft] == 0: passesLeft +=1
                if image[y][to_[0]+addXRight] == 0: passesRight +=1
            except: pass
        
        if passesLeft > 1:
            addXLeft += 10
        if passesRight > 1:
            addXRight += 10
        if passesRight <= 1 and passesLeft <= 1:
            break

    addYTop = 0
    addYBottom = 0
    while True:
        #counts how often the Bounding box passes through a line
        passesTop = 0
        passesBottom = 0
        for x in range(from_[0],to_[0]):
            try:
                if image[from_[1]-addYTop][x] == 0: passesTop +=1
                if image[to_[1]+addYBottom][x] == 0: passesBottom +=1
            except: pass
        if passesTop > 1:
            addYTop += 10
        if passesBottom > 1:
            addYBottom += 10
        if passesTop <= 1 and passesBottom <= 1:
            break

    return [[from_[0]-addXLeft,from_[1]-addYTop],[to_[0]+addXRight,to_[1]+addYBottom]]
