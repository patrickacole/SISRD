import numpy as np
from keras.layers import Input, Add, Conv2D, Deconv2D, UpSampling2D, BatchNormalization, LeakyReLU, Average
from keras.activations import relu
from keras.models import Model, load_model
from keras.optimizers import Adam
from keras.callbacks import Callback
from keras import backend as K
import h5py

from subpixel import SubpixelConv2D

_EPSILON = K.epsilon()
_W = 128
_H = 128

######################################################
# By default keras is using TensorFlow as a backend
######################################################

def generate_model():
    x_input = Input((64, 64, 1))

    conv1 = Conv2D(64, (5,5), padding='same', use_bias=True, activation='relu', name='conv1')(x_input)

    mid1 = Conv2D(32, (5,5), padding='same', use_bias=True, activation='relu', name='mid1')(conv1)
    mid2 = Conv2D(32, (3,3), padding='same', use_bias=True, activation='relu', name='mid2')(conv1)
    mid3 = Conv2D(32, (1,1), padding='same', use_bias=True, activation='relu', name='mid3')(conv1)

    merge = Average()([mid1, mid2, mid3])
    conv3 = Conv2D(16 , (3,3), padding='same', use_bias=True, activation='relu', name='conv3')(merge)
    subpix = SubpixelConv2D(conv3.shape, scale=2)(conv3)

    y_output = subpix

    model = Model(x_input, y_output)
    adam = Adam(lr=0.001)
    model.compile(optimizer=adam, loss=rmse, metrics=['accuracy'])
    return model

def rmse(y_true, y_pred):
    diff = K.square(255 * (y_pred - y_true))
    return K.sum(K.sqrt(K.sum(diff, axis=(2,1)) / (_W * _H)))

def loadModel(modelName):
    return load_model(modelName, custom_objects={'rmse': rmse})
    #return load_model(modelName)

def saveModel(model, modelName):
    model.save(modelName)

if __name__ == "__main__":
    print('test model')
    generate_model()
