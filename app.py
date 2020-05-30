import os
import sys
import  numpy as np
import pickle

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect


# Declare a flask app
app = Flask(__name__)


print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(bug_id):

    infile=open('models/pred','rb')
    x=pickle.load(infile)
    print(x)
    yp=np.argmax(x,axis=1)
    outfile=open('models/cl','rb')
    y=pickle.load(outfile)
    print(y)
    return y[yp[int(bug_id)]]


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
         bug_id = request.form.get('bug_id')
         devname = model_predict(bug_id)
         print(type(devname))
         return render_template('index.html', dev =devname.encode('utf-8').rstrip())

if __name__ == '__main__':
    app.run(port=5007, threaded=False)

    # Serve the app with gevent
    #http_server = WSGIServer(('0.0.0.0', 5000), app)
    #http_server.serve_forever()
