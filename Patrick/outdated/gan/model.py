import numpy as np
from keras.layers import Input, Add, Conv2D, Deconv2D, UpSampling2D, BatchNormalization, LeakyReLU
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

    conv1 = Conv2D(64, (5,5), padding='same', use_bias=True, name='conv1')(x_input)
    #bnconv1 = BatchNormalization(axis=3, name='bn_conv1')(conv1)
    rlconv1 = LeakyReLU(alpha=0.2, name='rl_conv1')(conv1)

    conv2 = Conv2D(64, (3,3), use_bias=True, name='conv2')(rlconv1)
    #bnconv2 = BatchNormalization(axis=3, name='bn_conv2')(conv2)
    rlconv2 = LeakyReLU(alpha=0.2, name='rl_conv2')(conv2)

    conv3 = Conv2D(64, (3,3), use_bias=True, name='conv3')(rlconv2)
    #bnconv3 = BatchNormalization(axis=3, name='bn_conv3')(conv3)
    rlconv3 = LeakyReLU(alpha=0.2, name='rl_conv3')(conv3)

    deconv1 = Deconv2D(64, (3,3), use_bias=True, name='deconv1')(rlconv3)
    #bndeconv1 = BatchNormalization(axis=3, name='bn_deconv1')(deconv1)
    rldeconv1 = LeakyReLU(alpha=0.3, name='rl_deconv1')(deconv1)
    sbdeconv1 = Add()([rldeconv1, rlconv2])

    deconv2 = Deconv2D(64, (3,3), use_bias=True, name='deconv2')(sbdeconv1)
    #bndeconv2 = BatchNormalization(axis=3, name='bn_deconv2')(deconv2)
    rldeconv2 = LeakyReLU(alpha=0.3, name='rl_deconv2')(deconv2)
    sbdeconv2 = Add()([rldeconv2, rlconv1])

    conv4 = Conv2D(4, (5,5), padding='same', use_bias=True, activation='relu', name='conv4')(sbdeconv2)
    y_output = SubpixelConv2D(conv4.shape, scale=2)(conv4)

    model = Model(x_input, y_output)
    adam = Adam(lr=0.0003)
    #model.compile(optimizer=adam, loss='mean_squared_error', metrics=['accuracy'])
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
    print('test imports')
    generate_model()
