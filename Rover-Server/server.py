from __future__ import print_function
import sys
sys.path.insert(0, 'lib')
from flask import Flask, render_template, redirect, Response
from flask_socketio import SocketIO, emit, join_room
import json
from threading import Thread


import base64

ROVER = '/rover'
BROWSER = '/browser'
VALUE_CHANGED = 'value changed'
ROVER_CONNECTED = 'rover connected'
ROVER_CONTROL = 'control'
ROVER_IMAGE = 'image'

TEMPLATE_VALUES = {
        'framerate': 15,
        'throttle_scale': 0.1,
        'steering_scale': 0.1,
        'neu_throttle': 90,
        'neu_steering': 90,
        'socketio_namespace': BROWSER,
        'value_changed': VALUE_CHANGED,
        'rover_connected': ROVER_CONNECTED,
        'rover_image': ROVER_IMAGE,
        }

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html', **TEMPLATE_VALUES)

@socketio.on('connect', namespace=BROWSER)
def browser_connected():
    app.logger.info('browser connected')
    join_room(BROWSER)

@socketio.on(VALUE_CHANGED, namespace=BROWSER)
def value_changed(message):
    steering = int(message.get('steering', 90))
    throttle = int(message.get('throttle', 90))
    #app.logger.info('value: {} {}'.format(steering, throttle))
    emit(ROVER_CONTROL, {'steering': steering, 'throttle': throttle}, namespace=ROVER, room=ROVER)

@socketio.on('connect', namespace=ROVER)
def rover_connect():
    app.logger.info('rover connected')
    join_room(ROVER)
    #TODO figure out how to emit this even if the browser hasn't connected yet
    # (need to figure out how to emit this on browser connect)
    emit(ROVER_CONNECTED, {}, namespace=BROWSER, room=BROWSER)

@socketio.on('disconnect', namespace=ROVER)
def rover_disconnect():
    app.logger.info('rover disconnected')

@socketio.on(ROVER_IMAGE, namespace=ROVER)
def rover_image(b64):
    app.logger.info('rover sent image')
    emit(ROVER_IMAGE, b64, namespace=BROWSER, room=BROWSER)

if __name__ == '__main__':
    app.logger.info('starting')
    socketio.run(app, host='0.0.0.0', debug=True)

