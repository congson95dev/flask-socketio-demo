from threading import Lock
from flask import Flask, render_template, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit, Namespace
import requests

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)

# Enable the cors so external system could access to our socketio
app.config["CORS_HEADERS"] = "Content-Type"
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")

thread = None
thread_lock = Lock()

url = 'https://api.coinbase.com/v2/prices/btc-usd/spot'


def background_thread(custom_namespace="/"):
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(2)
        count += 1
        price = ((requests.get(url)).json())['data']['amount']
        socketio.emit('my_response',
                      {'data': 'Bitcoin current price (USD): ' + price,
                       'count': count}, namespace=custom_namespace)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


'''
There's 2 approachs that has been implemented in this code:
1. The default feature of flask-socketio
2. The namespace feature of flask-socketio
'''


'''
1. The default feature of flask-socketio
'''
# @socketio.on('my_event')
# def handle_my_event(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']})
#
#
# '''
# There's 2 type of message, "default message" and "broadcast message"
# - Default message send a message only to the client who trigger this message
# - Broadcast message send a message to all clients
# '''
#
# # Send a message only to the client who trigger this message
# @socketio.on('default_message')
# def handle_message(data):
#     print('received message: ' + str(data))
#     emit('default_response', {'data': 'Default response sent'})
#
#
# # Broadcast a message to all clients
# @socketio.on('broadcast_message')
# def handle_broadcast(data):
#     print('received: ' + str(data))
#     emit('broadcast_response', {'data': 'Broadcast sent'}, broadcast=True)
#
#
# # @socketio.event is the same as @socketio.on, but it have some difference which is
# # it's used to handle the event that already defined by the flask-socketio
# # such as connect(), the connect() event is used when the client
# # want to connect to the server
# @socketio.event
# def connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(background_thread)
#     emit('my_response', {'data': 'Connected', 'count': 0})


'''
2. The namespace feature of flask-socketio
'''

custom_namespace = '/private'


class PrivateNamespace(Namespace):
    def on_connect(self):
        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(background_thread, custom_namespace)
        emit('my_response', {'data': 'Connected', 'count': 0})
        pass

    def on_my_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']})

    def on_default_message(self, data):
        print('received message: ' + str(data))
        emit('default_response', {'data': 'Default response sent'})

    def on_broadcast_message(self, data):
        print('received: ' + str(data))
        emit('broadcast_response', {'data': 'Broadcast sent'}, broadcast=True)


socketio.on_namespace(PrivateNamespace(custom_namespace))


if __name__ == '__main__':
    socketio.run(app)

