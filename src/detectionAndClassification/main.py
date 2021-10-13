import knn as knn
import numpy as np


caps = knn.getImageCategory("./trainingsImages/caps","cap",1)
res = knn.getImageCategory("./trainingsImages/caps","resistor",1)
trainingData = np.concatenate((caps,res))

testImage = knn.loadImage(".","test")

classifier = knn.KNN(trainingPairs=trainingData)

print(knn.evaluate(classifier,testImage=testImage))