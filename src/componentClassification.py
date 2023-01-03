import sys
sys.path.append('../')

import tensorflow as tf
from keras.models import load_model

import numpy as np
import cv2
from lib.constants import CLASS_NAMES


def convertImg(image, size=(32,32)):
    image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    converted = np.zeros(shape=(size[0], size[1], 1))
    for y in range(0, len(image)):
        for x in range(0, len(image[y])):
            converted[y][x][0] = image[y][x]

    converted = converted/255
    return converted

def loadModel():
    model = load_model('./../resources/saved_model/my_model.h5')
    return model

def predict(box, image, model):

    component = convertImg(image[box[0][1]:box[1][1], box[0][0]:box[1][0]]).reshape(-1,32,32,1)
    model_prediction = model.predict(component)[0]

    prediction = (CLASS_NAMES[np.argmax(model_prediction)])
    #prediction = [CLASS_NAMES[np.argmax(model_prediction[:-4])],CLASS_NAMES[-4:][np.argmax(model_prediction[-4:])]]

    return prediction#[0], ROTATION_DICT[prediction[1]]

def classify(boxes, image, model):

    components = []
    for box in boxes:
        component = image[box[0][1]:box[1][1], box[0][0]:box[1][0]]
        components.append(convertImg(component).reshape(-1,32,32,1))

    modelPredictions = model.predict(np.vstack(components))

    predictions = []

    for prediction in modelPredictions:
        
        predictions.append(CLASS_NAMES[np.argmax(prediction)])
        #predictions.append([CLASS_NAMES[np.argmax(prediction[:-4])],CLASS_NAMES[-4:][np.argmax(prediction[-4:])]])


    return predictions