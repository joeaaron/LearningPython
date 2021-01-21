#!/usr/bin/env python
from importlib import import_module
import os, time, threading
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from threading import Lock
from gevent import monkey
from gevent.pywsgi import WSGIServer
import numpy as np
from multiprocessing import Process
#from geventwebsocket.handler import WebSocketHandler

monkey.patch_all()

# import camera driver
from camera_opencv import Camera


app = Flask(__name__)

thread = None
thread_lock = Lock()
socketio = SocketIO(app)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def background_thread():
    x= 0
    y =87
    while True:
        socketio.sleep(0.2)
        t = time.strftime('%M:%S', time.localtime()) 
        if(x%5 == 0):
            socketio.emit('server_response', {'pos': [x,y]} )

        x += 1
        #y += 2
        x %=200
        #y %=200
        #print 'hello'
        
@socketio.on('connect_event')
def connected_msg(msg):
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
            
def camear1():
    os.system('python camera1.py')
    
def camear2():
    os.system('python camera2.py')
    
if __name__ == '__main__':
    Process(target = camear1).start()
    Process(target = camear2).start()
    #socketio.run(app,debug=False,host='0.0.0.0', port=5000)
    http_server = WSGIServer(('0.0.0.0', 70), app)
    http_server.serve_forever()
    #app.run(host='0.0.0.0', port=5000)
