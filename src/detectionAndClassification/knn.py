from PIL import Image
from numpy import asarray, argmin

class KNN():
    def __init__(self,trainingPairs) -> None:
        self.trainingPairs = trainingPairs


def getImageCategory(path,label,count):
    trainData = []
    for x in range(0,count):
        image = Image.open('{path}/{x}.png'.format(path=path,x=x)).convert('L')
        data = 1 - asarray(image)/255
        trainData.append([label,data])
    return trainData


def _distance(referenceImage,otherImage):
    size = len(referenceImage)
    sum_ = 0;
    for x in range(0,size):
        othersize = len(referenceImage[x])
        for y in range(0,othersize):
            sum_ += (referenceImage[x,y] - otherImage[x,y])**2
    return math.sqrt(sum_)

# returns a label, certainty pair
def evaluate(knn, testImage) -> tuple((str,float)):
    trainImages = list(map(lambda x: x[1],knn.trainingPairs))
    trainLables = list(map(lambda x: x[0],knn.trainingPairs))

    distances = list(map(lambda x: _distance(testImage,x),trainImages))

    # Find minimal distance,get index and get the Lable of the training Image
    min_index = argmin(distances)
    min_dist = min(distances)

    #get sencond min
    del distances[min_index]
    second_min_dist = min(distances)

    #get maximum
    max_dist = max(distances)

    certainty = 100*(second_min_dist-min_dist)/(max_dist-min_dist)

    return (trainLables[min_index],certainty)
