# Smarter Circuits #
import sys
sys.path.append('../')


import imagePreprocessing as ip
import graphGeneration as gg
import componentClassification as cc
import cv2
import lib.utils as utils

image = utils.loadImage(path="./../resources/testImages",name="1.png")

colorImage = utils.loadImage(path="./../resources/testImages",name="1.png", color=True)

preprocessedImage = ip.preprocessImage(image)

utils.saveImage(name="preprocessed.png", image=preprocessedImage)

boundingBoxes = gg.generateBoudingBoxes(preprocessedImage)

predictions = cc.classify(boundingBoxes, image)

print(len(boundingBoxes))

for i in range(0, len(boundingBoxes)):
    if predictions[0] == "ground":
        utils.drawRect(colorImage,boundingBoxes[i],(255,0,0))
    elif predictions[0] == "resistor":
        utils.drawRect(colorImage,boundingBoxes[i],(0,255,0))
    elif predictions[0] == "capacitor":
        utils.drawRect(colorImage,boundingBoxes[i],(0,0,244))
    


colorImage = cv2.cvtColor(colorImage, cv2.COLOR_BGR2RGB)

utils.saveImage(name="boundingBoxes.png", image=colorImage, color=True)