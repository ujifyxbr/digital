import os
import cv2
import base64
import PIL

from flask import Flask, request, Response

import config
import main
import models
import db

app = Flask(__name__)

@app.route("/learn", methods=['POST'])
def learn():
    data = request.get_json(force=True)
    response = main.process_learn_images(data)
    return Response(status=200)

@app.route("/process", methods=['POST'])
def process():
    data = request.get_json(force=True)
    response = main.process_frame(data)
    return Response(status=200)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.db_session.remove()

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000, debug=True)