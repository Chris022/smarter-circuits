import math as m

class DirGradient:
    def __init__(self):
        self.queueX = []
        self.queueY = []

    def addStep(self,currentPosition,lastPosition):
        #get Direction
        xDir = 0
        yDir = 0

        if currentPosition[0] - lastPosition[0] > 0:
            xDir = 1
        elif currentPosition[0] - lastPosition[0] < 0:
            xDir = -1

        if currentPosition[1] - lastPosition[1] > 0:
            yDir = 1
        elif currentPosition[1] - lastPosition[1] < 0:
            yDir = -1

        self.queueX.append(xDir)
        self.queueY.append(yDir)
    
    def checkForEdge(self):
        #only gives a valid answer if there are more than 10 previous values
        if len(self.queueX) < 10: return False

        cSumX = sum(self.queueX[-5:]) # the latest 5 X coordinates
        cSumY = sum(self.queueY[-5:]) # the latest 5 Y coordinates
        length = m.sqrt(cSumX**2 + cSumY**2)
        currDir = (cSumX/length, cSumY/length)

        
        lSumX = sum(self.queueX[-10:-5]) # the 5 X coords 5 steps ago
        lSumY = sum(self.queueY[-10:-5]) # the 5 Y coords 5 steps ago
        length = m.sqrt(cSumX**2 + cSumY**2)
        lastDir = (lSumX/length, lSumY/length)

        dist = m.sqrt((currDir[0] - lastDir[0])**2 + (currDir[1] - lastDir[1])**2)

        if dist <= 0.7:
            return False

        return True

    def reset(self):
        self.queueX = []
        self.queueY = []