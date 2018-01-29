#!/usr/bin/env python
from importlib import import_module
import os, time
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from threading import Lock
from gevent import monkey
from gevent.pywsgi import WSGIServer
#from geventwebsocket.handler import WebSocketHandler

monkey.patch_all()

# import camera driver
from camera_opencv import Camera, Camera1


app = Flask(__name__)

camears = [Camera('tree.avi'), Camera('xing.avi')]

thread = None
thread_lock = Lock()
socketio = SocketIO(app)
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        time.sleep(0.2)
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
			   
@app.route('/video_feed1')
def video_feed1():
    """Video streaming routeSSS. Put this in the src attribute of an img tag."""
    return Response(gen(camears[1]), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camears[0]), mimetype='multipart/x-mixed-replace; boundary=frame')


def background_thread():
    x= 0
    y =0
    while True:
        socketio.sleep(0.2)
        t = time.strftime('%M:%S', time.localtime()) 
        socketio.emit('server_response', {'pos': [x,y]} )
        x += 1
        y += 2
        x %=200
        y %=200
        #print 'hello'
        
@socketio.on('connect_event')
def connected_msg(msg):
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


if __name__ == '__main__':
    #socketio.run(app,debug=False,host='0.0.0.0', port=5000)
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
    #app.run(host='0.0.0.0', port=5000)
