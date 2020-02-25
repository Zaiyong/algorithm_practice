import json
from flask import Flask, request
from flask import Response
from keras.models import load_model

import numpy as np
import pandas as pd

app = Flask(__name__)
img_width, img_height = 28, 28


def loadModel():
    model=load_model('./digital-recognizer-model.h5')
    model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
    return model

model=loadModel()

@app.route('/predict', methods=['POST'])
def predict():
    input=request.get_json()
    input_array = np.array(list(input.values()))
    input_ndarray=input_array.reshape(-1,28,28,1)
    pred=model.predict(input_ndarray,batch_size=128)
    result={'digital':-1}
    print(pred[0])
    for i in range(len(pred[0])):
        if pred[0][i]==1:
            result['digital']=i
    print(result)
    return Response(json.dumps(result),mimetype='application/json')

if __name__=='__main__':
    app.run()
