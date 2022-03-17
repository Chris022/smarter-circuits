from tkinter import *
import cv2

from lib.gui.guiUtils import *

import src.imagePreprocessing as ip
import src.graphGeneration as gg
import src.patternMatching as pm
import src.boundingBoxGeneration as bbg
import src.cuircitGeneration as cg
import src.componentClassification as cc

import copy

import lib.utils as utils
import numpy as np

import _thread as thread

import subprocess

import random
import string

import igraph

import time
from lib.gui.popup import createPopUp


class DetectCircuit():

    def __init__(self, root, position):

        self.position = position
        
        self.canvas = Canvas(root)

        self.detect = Button(root, text='Detect Circuit', command=self.start_detection)


    def add(self, image):
        self.original_image = image

        self.image_offset = (0,0)

        self.image_width = len(image[0])
        self.image_height = len(image)

        self.canvas.configure(bg='#8f8f8f')

        self.tkImg = convert_to_tkImg(self.original_image)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=CENTER, image=self.tkImg)
        

        self.canvas.place(relx=self.position[0], rely=self.position[1], relwidth=self.position[2], relheight=self.position[3])
        self.canvas.update()
        self.resize(self.original_image)

        self.detect.place(relx=0.8, rely=0.15, relwidth=0.1, relheight=0.05)

    def start_detection(self):
        thread.start_new_thread(self.detect_circuit, ())

    def generateTrainData(self, boundingBoxes, image):
        for box in boundingBoxes:
            component = image[box[0][1]:box[1][1], box[0][0]:box[1][0]]
            component = cv2.resize(component, (32,32), interpolation = cv2.INTER_AREA)
            #utils.saveImage(path='./../resources/trainData/')
            utils.saveImage(path='./../resources/trainData/', name="{i}.png".format(i=''.join(random.choice(string.ascii_lowercase) for i in range(10))), image=component)

    def drawRect(self, image,boundingBoxes,color):
        corner1 = boundingBoxes[0]
        corner2 = boundingBoxes[1]
        startX = corner1[0]
        startY = corner1[1]

        endX = corner2[0]
        endY = corner2[1]

        for x in range(startX,endX):
            image[startY][x] = color
            image[endY][x] = color

        for y in range(startY,endY):
            image[y][startX] = color
            image[y][endX] = color

        return image

    def detect_circuit(self):

        try:
            start_time = time.time()
            print("Start detection")

            image = self.original_image
            s1 = np.full((len(image),10),255)
            image = np.insert(image, [0], s1, axis=1)
            image = np.insert(image, [len(image[0])], s1, axis=1)
            s2 = np.full((10,len(image[0])),255)
            image = np.insert(image, [0], s2, axis=0)
            image = np.insert(image, [len(image)], s2, axis=0)

            utils.saveImage(name="binary.png", image=image)

            preprocessedImage = ip.preprocessImage(image.copy())

            print("Preprocessed")
            print("--- %s seconds ---" % (time.time() - start_time))
            start_time = time.time()

            #test
            utils.saveImage(name="preprocessed.png", image=preprocessedImage)

            graph = gg.generateGraph(preprocessedImage)
            matches_ = pm.getComponents(graph)
            boundingBoxes_ = utils.fmap(lambda x: bbg.generateBoundingBox(x,preprocessedImage),matches_)

            print("Bounding Boxes")
            print("--- %s seconds ---" % (time.time() - start_time))
            start_time = time.time()

            igraphUnion = utils.convertToIgraph(graph)
            layout = igraphUnion.layout("large_graph")
            igraph.plot(igraphUnion, "graph.png",layout=layout, bbox = (1000,1000), vertex_label=None)


            #self.generateTrainData(boundingBoxes_, image)

            for boundingBox in boundingBoxes_:
                img = self.drawRect(image,boundingBox,0)
            utils.saveImage(name="box.png", image=img)

            cc.loadModel()

            predictions = []

            for box in boundingBoxes_:
                buildingType = cc.predict(box,image)
                #print(buildingType)
                predictions.append(buildingType)

            print("Predictions")
            print("--- %s seconds ---" % (time.time() - start_time))
            start_time = time.time()


            graph = cg.createLTSpiceFile(matches_,boundingBoxes_,predictions,copy.copy(graph),"./out.asc")

            print("File Generated")
            print("--- %s seconds ---" % (time.time() - start_time))
            start_time = time.time()

            subprocess.call(["C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe","./out.asc"])
        except Exception as e:
            createPopUp(str(e))
    def resize(self, *arg):

        img = self.original_image

        if len(arg) != 0:
            img = arg[0]

        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.canvas.coords(self.image_on_canvas, (int)(self.canvas_width/2), (int)(self.canvas_height/2))

        factor = 1

        if self.image_width > self.image_height:
            factor = self.canvas_width/self.tkImg.width()
            k = self.image_height * (self.canvas_width/self.image_width)
            resized_image = cv2.resize(img, ((int)(self.canvas_width),(int)(k)), interpolation=cv2.INTER_AREA)
            self.tkImg = convert_to_tkImg(resized_image)
        else:
            factor = self.canvas_height/self.tkImg.height()
            k = self.image_width * (self.canvas_height/self.image_height)
            resized_image = cv2.resize(img, ((int)(k), (int)(self.canvas_height)), interpolation=cv2.INTER_AREA)
            self.tkImg = convert_to_tkImg(resized_image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.tkImg)
    

    def remove(self):
        self.canvas.place_forget()
        self.detect.place_forget()

        return -1