#!/usr/bin/env python
import time
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='./')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('client_event')
def client_msg(msg):
    while 1:
        emit('server_response', {'data': msg['data']})
        time.sleep(0.5)
    
@socketio.on('connect_event')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')