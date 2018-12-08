import numpy as np
import loss
from subpixel import SubpixelConv2D
from keras.layers import Add, Input, Conv2D, Deconv2D, MaxPooling2D, UpSampling2D, PReLU, BatchNormalization
from keras.optimizers import Adam
from keras.models import Model, load_model

######################################################
# By default keras is using TensorFlow as a backend
######################################################

######################################################
# Implementing model in
# "Medical image denoising using convolutional denoising autoencoders"
# CNNDAE
######################################################
def CNNDAE():
    x_input = Input((128, 128, 1))

    conv1 = Conv2D(64, (7, 7), padding='same', activation='relu')(x_input)
    mp1   = MaxPooling2D(pool_size=(2, 2))(conv1)
    conv2 = Conv2D(64, (5, 5), padding='same', activation='relu')(mp1)
    mp2   = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(64, (7, 7), padding='same', activation='relu')(mp2)
    up1   = UpSampling2D(size=(2, 2))(conv3)
    conv4 = Conv2D(64, (7, 7), padding='same', activation='relu')(up1)
    up2   = UpSampling2D(size=(2, 2))(conv4)

    conv5 = Conv2D(1, (5, 5), padding='same', activation='relu')(up2)

    model = Model(x_input, conv5)

    model.compile(loss=loss.rmse, optimizer=Adam(lr=0.001), metrics=['accuracy'])

    return model

######################################################
# Implementing model in
# https://github.com/titu1994/Image-Super-Resolution
# Denoiseing (Auto Encoder) Super Resolution CNN (DSRCNN)
######################################################
def DSRCNN():
    x_input = Input((64, 64, 1))

    conv1   = Conv2D(64, (3, 3), padding='same', use_bias=True, activation='relu')(x_input)
    conv2   = Conv2D(64, (3, 3), padding='same', use_bias=True, activation='relu')(conv1)
    deconv1 = Deconv2D(64, (3, 3), padding='same', use_bias=True)(conv2)
    
    add1    = Add()([conv2, deconv1])
    deconv2 = Deconv2D(64, (3, 3), padding='same', use_bias=True)(add1)
    
    add2  = Add()([conv1, deconv2])
    conv3 = Conv2D(4, (3, 3), padding='same', use_bias=True, activation='relu')(add2)
    spc1  = SubpixelConv2D(conv3.shape, scale=2)(conv3)

    model = Model(x_input, spc1)

    model.compile(loss=loss.rmse, optimizer=Adam(lr=0.001), metrics=['accuracy']) # v1 -> lr=0.003, v2 -> lr=0.001

    return model

######################################################
# Implementing model in
# https://github.com/titu1994/Image-Super-Resolution
# Denoiseing (Auto Encoder) Super Resolution CNN (DSRCNN)
######################################################
def DDSRCNN():
    x_input = Input((64, 64, 1))

    conv1 = Conv2D(64, (5, 5), padding='same', use_bias=True, activation='relu')(x_input)
    conv2 = Conv2D(64, (5, 5), padding='same', use_bias=True, activation='relu')(conv1)

    mp1   = MaxPool2D(pool_size=(2, 2), padding='same')(conv2)
    conv3 = Conv2D(128, (3, 3), padding='same', use_bias=True, activation='relu')(mp1)
    conv4 = Conv2D(128, (3, 3), padding='same', use_bias=True, activation='relu')(conv3)

    mp2   = MaxPool2D(pool_size=(2, 2), padding='same')(conv4)
    conv5 = Conv2D(256, (3, 3), padding='same', use_bias=True, activation='relu')(mp2)
    spc1  = SubpixelConv2D(conv5.shape, name='spc1', scale=2)(conv5)
    conv6 = Conv2D(128, (3, 3), padding='same', use_bias=True)(spc1)
    conv7 = Conv2D(128, (3, 3), padding='same', use_bias=True)(conv6)

    add1 = Add()([conv4, conv7])

    spc2  = SubpixelConv2D(add1.shape, name='spc2', scale=2)(add1)
    conv8 = Conv2D(64, (3, 3), padding='same', use_bias=True)(spc2)
    conv9 = Conv2D(64, (3, 3), padding='same', use_bias=True)(conv8)

    add2   = Add()([conv2, conv9])
    conv10 = Conv2D(4, (3, 3), padding='same', use_bias=True)(add2)
    spc3   = SubpixelConv2D(conv10.shape, name='spc3', scale=2)(conv10)

    model = Model(x_input, spc3)

    model.compile(loss=loss.rmse, optimizer=Adam(lr=0.001), metrics=['accuracy'])

    return model

######################################################
# Implementing model in
# "Deep Learning for Single Image Super-Resolution:
#  A Brief Review" SRResNet - Fig.5c
# SRResNet
######################################################
def SRResNet():
    # takes input of 128x128
    x_input = Input((128, 128, 1))

    conv1  = Conv2D(1, (3, 3), padding='same', activation='relu')(x_input)
    prelu1 = PReLU(alpha_initializer='zeros')(conv1)

    conv2  = Conv2D(16, (3, 3), padding='same', activation='relu')(prelu1)
    bn1    = BatchNormalization(axis=3)(conv2)
    prelu2 = PReLU(alpha_initializer='zeros')(bn1)
    conv3  = Conv2D(16, (3, 3), padding='same', activation='relu')(prelu2)
    bn2    = BatchNormalization(axis=3)(conv3)

    add1  = Add()([prelu1, bn2])
    conv4 = Conv2D(1, (3, 3), padding='same', activation='relu')(add1) # v1, 10 epochs
    # conv5 = Conv2D(1, (3, 3), padding='same', activation='relu')(conv4) # v1, 10 epochs; v2, 40 epochs
    bn3   = BatchNormalization(axis=3)(conv4) # v3, 40 epochs

    add2  = Add()([prelu1, bn3]) # v3, 40 epochs
    conv5 = Conv2D(1, (3, 3), padding='same', activation='relu')(add2) # v3, 40 epochs

    model = Model(x_input, conv5)

    # model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.001), metrics=['accuracy']) #v1-3
    model.compile(loss=loss.rmse, optimizer=Adam(lr=0.001), metrics=['accuracy']) # v4

    return model

def loadModel(name):
    return load_model(name, custom_objects={'rmse': loss.rmse})
    # return load_model(name)

lookup = dict()
lookup['CNNDAE']   = CNNDAE
lookup['DSRCNN']   = DSRCNN
lookup['DDSRCNN']  = DDSRCNN
lookup['SRResNet'] = SRResNet

if __name__ == "__main__":
    cnndae   = lookup['CNNDAE']
    dsrcnn   = lookup['DSRCNN']
    ddsrcnn  = lookup['DDSRCNN']
    srresnet = lookup['SRResNet']