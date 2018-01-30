#!/usr/bin/env python
from importlib import import_module
import sys, os, time
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from threading import Lock
from gevent import monkey
from gevent.pywsgi import WSGIServer
import numpy as np
#from geventwebsocket.handler import WebSocketHandler

monkey.patch_all()

# import camera driver
from camera_opencv import Camera


app = Flask(__name__)

pwd = sys.path[0]

camears = [Camera('videos/car2.avi')]

def gen(camera):
    """Video streaming generator function."""
    while True:
        time.sleep(0.02)
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
			   
@app.route('/video_feed')
def video_feed():
    """Video streaming routeSSS. Put this in the src attribute of an img tag."""
    return Response(gen(camears[0]), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    #socketio.run(app,debug=False,host='0.0.0.0', port=5000)
    http_server = WSGIServer(('0.0.0.0', 5002), app)
    http_server.serve_forever()
    #app.run(host='0.0.0.0', port=5000)
