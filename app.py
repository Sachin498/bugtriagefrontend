import os
import sys
import  numpy as np
import pickle
import json
from collections import defaultdict


# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect


# Declare a flask app
app = Flask(__name__)


print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(bug_id):
    values = defaultdict()
    
    infile=open('models/pred','rb')
    x=pickle.load(infile)
    #print(x)
    yp=np.argmax(x,axis=1)
    outfile=open('models/cl','rb')
    y=pickle.load(outfile)
    
    jsonFile = open('models/deep_data.json','rb')
    temp = json.load(jsonFile,strict=False)
    #print(y)
    
    for entry in temp:
        values[entry['id']] = {
            'issue_id' : entry['issue_id'],
            'issue_title' : entry['issue_title'],
            'reported_time' : entry['reported_time'],
            'owner' : entry['owner'],
            'description' : entry['description']
        }
      
    #for key in values.keys():
    #    print(values[key]['description'])
    #print(values[bug_id]['description'])
    nam="The assigned developer is "
    name = nam+y[yp[int(bug_id)]]
    desc = "The Bug Description is "+values[bug_id]['description']
    return (name , desc)


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
         bug_id = int(request.form.get('bug_id'))
         devname,description = model_predict(bug_id)
         return render_template('index.html', dev =devname, desc=description)

if __name__ == '__main__':
    app.run(host='localhost',debug=True,threaded=True)

    # Serve the app with gevent
    #http_server = WSGIServer(('0.0.0.0', 5000), app)
    #http_server.serve_forever()
