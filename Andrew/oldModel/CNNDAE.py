import numpy as np
import loss
from keras.layers import Input, MaxPooling2D, UpSampling2D, Conv2D, Flatten, Dense
from keras.optimizers import Adam
from keras.models import Model, load_model

######################################################
# By default keras is using TensorFlow as a backend
######################################################

######################################################
# Implementing model in
# "Medical image denoising using convolutional denoising autoencoders"
######################################################

def createModel():
    # takes input of 128x128
    x_input = Input((128, 128, 1))
    conv1 = Conv2D(64, (7, 7), padding='same', activation='relu')(x_input)
    mp1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    conv2 = Conv2D(64, (5, 5), padding='same', activation='relu')(mp1)
    mp2 = MaxPooling2D(pool_size=(2, 2))(conv2)
    conv3 = Conv2D(64, (7, 7), padding='same', activation='relu')(mp2)
    up1 = UpSampling2D(size=(2, 2))(conv3)
    conv4 = Conv2D(64, (7, 7), padding='same', activation='relu')(up1)
    up2 = UpSampling2D(size=(2, 2))(conv4)
    conv5 = Conv2D(1, (5, 5), padding='same', activation='relu')(up2)

    model = Model(x_input, conv5)

    # model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.001), metrics=['accuracy'])
    model.compile(loss=loss.rmse, optimizer=Adam(lr=0.001), metrics=['accuracy'])

    return model

if __name__ == "__main__":
    model = createModel()
