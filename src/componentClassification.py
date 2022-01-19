import sys
sys.path.append('../')

import tensorflow as tf
from tensorflow.keras import layers, models

import numpy as np
import cv2
from lib.constants import CLASS_NAMES, ROTATION_DICT

model = None


def convertImg(image, size=(32,32)):
    image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    converted = np.zeros(shape=(size[0], size[1], 1))
    for y in range(0, len(image)):
        for x in range(0, len(image[y])):
            converted[y][x][0] = image[y][x]

    converted = converted/255
    return converted


def loadModel():
    global model
    model = tf.keras.models.load_model('./../resources/saved_model/my_model')

def predict(box, image):
    global model

    component = convertImg(image[box[0][1]:box[1][1], box[0][0]:box[1][0]]).reshape(-1,32,32,1)
    model_prediction = model.predict(component)[0]

    prediction = [CLASS_NAMES[np.argmax(model_prediction[:-4])],CLASS_NAMES[-4:][np.argmax(model_prediction[-4:])]]

    return prediction[0], ROTATION_DICT[prediction[1]]

def classify(boxes, image):
    global model

    components = []
    for box in boxes:
        component = image[box[0][1]:box[1][1], box[0][0]:box[1][0]]
        components.append(convertImg(component).reshape(-1,32,32,1))

    modelPredictions = model.predict(np.vstack(components))

    predictions = []

    for prediction in modelPredictions:
        
        predictions.append([CLASS_NAMES[np.argmax(prediction[:-4])],CLASS_NAMES[-4:][np.argmax(prediction[-4:])]])

        #predictions.append(class_names[np.argmax(prediction)])

    return predictions