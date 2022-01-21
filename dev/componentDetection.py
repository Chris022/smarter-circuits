import sys
sys.path.append('../')

import tensorflow as tf

from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import lib.utils as utils
from lib.constants import S, B, C, INPUT_SIZE, CLASS_NAMES,CLASS_COLORS, LAMBDA_COORD, LAMBDA_NOOBJ
import os
import cv2
import math
import pickle

label_names = os.listdir('./../resources/labeled_data/labels')
print(label_names)

labels = []
for label_name in label_names:
    file = open(str('./../resources/labeled_data/labels/' + label_name), 'rb')
    label = pickle.load(file)
    file.close()
    labels.append(label)

image_names = os.listdir('./../resources/labeled_data/images')
print(image_names)

images = []
for image_name in image_names:
    image = utils.loadImage(path='./../resources/labeled_data/images', name=image_name, resize=(INPUT_SIZE,INPUT_SIZE),color=False)
    images.append(image)

if len(images) != len(labels):
    sys.exit('#labels != #images')


#only works for B=1
def get_output_tensor(label):
    shape = (S,S,5*B+C)
    out = np.zeros(shape)

    cell_size = (int)(INPUT_SIZE/S)
    for box in label:
        x_cell = math.floor(box['b_x']/cell_size)
        y_cell = math.floor(box['b_y']/cell_size)

        if not np.array_equal(out[x_cell][y_cell], np.zeros(5*B+C)):
            sys.exit('More then one bounding box in cell')

        y = np.zeros(5*B+C)
        y[CLASS_NAMES.index(box['c'])-C] = 1

        y[0] = 1
        y[1] = (box['b_x'] - cell_size*x_cell) / cell_size
        y[2] = (box['b_y'] - cell_size*y_cell) / cell_size
        y[3] = box['b_w'] / INPUT_SIZE
        y[4] = box['b_h'] / INPUT_SIZE
        
        out[x_cell][y_cell] = y
    return out.flatten()

train_images = []
train_labels = []

for i in range(0, len(images)):
    train_images.append(images[i]/255)
    train_labels.append(get_output_tensor(labels[i]))

train_images = np.asarray(train_images)
train_labels = np.asarray(train_labels)

print(train_images.shape)
print(train_labels.shape)

def leaky_reLu(x):
    return tf.keras.activations.relu(x, alpha=0.1)

model = models.Sequential()

model.add(layers.Conv2D(filters=64, kernel_size=(7, 7), activation=leaky_reLu, input_shape=(INPUT_SIZE, INPUT_SIZE, 1)))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

#model.add(layers.Conv2D(filters=192, kernel_size=(3, 3), activation=leaky_reLu))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))


model.add(layers.Conv2D(filters=128, kernel_size=(3, 3), activation=leaky_reLu))
#model.add(layers.Conv2D(filters=256, kernel_size=(3, 3), activation=leaky_reLu))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Conv2D(filters=256, kernel_size=(3, 3), activation=leaky_reLu))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(filters=256, kernel_size=(3, 3), activation=leaky_reLu))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

#model.add(layers.Conv2D(filters=512, kernel_size=(3, 3), activation=leaky_reLu))
model.add(layers.Conv2D(filters=1024, kernel_size=(3, 3), activation=leaky_reLu))
model.add(layers.Flatten())

model.add(layers.Dense(5*S*S*(5*B+C), activation=leaky_reLu))
model.add(layers.Dense(S*S*(5*B+C), activation='sigmoid'))

print('created')

def loss(y_true, y_pred):
  
  y_true = tf.reshape(y_true, (-1, S, S, 5*B+C))
  y_pred = tf.reshape(y_pred, (-1, S, S, 5*B+C))

  exists_box = y_true[...,0:1]

  y_pred_obj = tf.multiply(y_pred, exists_box)

  y_pred_no_obj = tf.multiply(y_pred, tf.subtract(1, exists_box))
  y_pred_no_obj = tf.add(y_pred_no_obj, tf.multiply(tf.cast(tf.fill(((1, S, S, 5*B+C)),1), 'float32') ,exists_box))

  #box loss
  box_loss1 = tf.math.reduce_sum(tf.math.squared_difference(y_true[...,1:3], y_pred_obj[...,1:3]))
  box_loss2 = tf.math.reduce_sum(tf.math.squared_difference(tf.math.sqrt(tf.math.abs(y_true[...,3:5])), tf.math.sqrt(tf.math.abs(y_pred_obj[...,3:5]))))

  box_loss = tf.math.add(box_loss1, box_loss2)

  #object loss
  object_loss = tf.math.reduce_sum(tf.math.squared_difference(y_true[...,0:1], y_pred_obj[...,0:1]))

  #no object loss
  no_object_loss = tf.math.reduce_sum(tf.math.squared_difference(y_true[...,0:1], y_pred_no_obj[...,0:1]))

  #class loss
  class_loss = tf.math.reduce_sum(tf.math.squared_difference(y_true[...,5:10], y_pred_obj[...,5:10]))

  loss = tf.math.add_n([tf.math.multiply(LAMBDA_COORD, box_loss), tf.math.multiply(LAMBDA_NOOBJ, no_object_loss), object_loss, class_loss])

  return loss#tf.reduce_sum(loss)# / tf.reduce_sum(mask)

model.compile(optimizer='adam',
              #loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              loss=loss,
              run_eagerly=True,
              metrics=['accuracy'])

train_labels = tf.convert_to_tensor(train_labels)

#print(train_labels)
train_images = tf.expand_dims(train_images, axis=-1)

#x = model.predict(train_images)
#print(x)

#history = model.fit(train_images, train_labels, epochs=10, 
#                    validation_data=(test_images, test_labels))

history = model.fit(train_images, train_labels, batch_size=6, epochs=1, use_multiprocessing=True)

print('trained')

model.save('./../resources/saved_model/my_model')

print('saved')

#model = tf.keras.models.load_model('./../resources/saved_model/my_model')

#test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)