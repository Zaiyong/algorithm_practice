
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization


def preProcessData(train_file='./train.csv',test_file='./test.csv',image_size=[28,28]):
    data_train = pd.read_csv(train_file)
    data_test = pd.read_csv(test_file)

    img_rows, img_cols = image_size
    input_shape = (img_rows, img_cols, 1)

    X = np.array(data_train.iloc[:, 1:])
    y = to_categorical(np.array(data_train.iloc[:, 0]))

    #Here we split validation data to optimiza classifier during training
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=13)

    #Test data
    X_test = np.array(data_test.iloc[:, 1:])
    y_test = to_categorical(np.array(data_test.iloc[:, 0]))



    X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
    X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
    X_val = X_val.reshape(X_val.shape[0], img_rows, img_cols, 1)

    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_val = X_val.astype('float32')
    X_train /= 255
    X_test /= 255
    X_val /= 255
    return X_train, y_train, X_val, y_val, X_test, y_test

def build_model(X_train,y_train,X_val, y_val,image_size=[28,28]):
    batch_size = 256
    num_classes = 10
    epochs = 50

    #input image dimensions
    img_rows, img_cols = image_size
    input_shape = (img_rows, img_cols, 1)
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     kernel_initializer='he_normal',
                     input_shape=input_shape))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(Dropout(0.4))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adam(),
                  metrics=['accuracy'])
    model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(X_val, y_val))
    return model

if __name__=='__main__':
    X_train, y_train, X_val, y_val, X_test, y_test=preProcessData('./train.csv','./test.csv')
    build_model(X_train, y_train, X_val, y_val)
