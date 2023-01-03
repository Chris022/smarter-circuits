# Smarter Circuits #
import sys
sys.path.append('../')


import imagePreprocessing as ip
import graphGeneration as gg
import cuircitGeneration as cg
import componentClassification as cc
import cv2
import lib.utils as utils
import numpy as np

#image = utils.loadImage(path="./../resources/testImages",name="1.png")
#
#colorImage = utils.loadImage(path="./../resources/testImages",name="1.png", color=True)

def detectCircuit(image):

    s1 = np.full((len(image),10),255)
    image = np.insert(image, [0], s1, axis=1)
    image = np.insert(image, [len(image[0])], s1, axis=1)
    s2 = np.full((10,len(image[0])),255)
    image = np.insert(image, [0], s2, axis=0)
    image = np.insert(image, [len(image)], s2, axis=0)


    preprocessedImage = ip.preprocessImage(image)

    graph = gg.generateGraph(preprocessedImage)
    components = gg.getComponents(graph)

    cc.loadModel()

    predictions = []

    for comp in components:
        box = comp[0]
        matches = comp[1]
        buildingType = cc.predict(box,image)#[0]
        predictions.append((box,matches,buildingType))#,rot))


    graph = cg.createLTSpiceFile(predictions,graph,"./out.asc")
        


