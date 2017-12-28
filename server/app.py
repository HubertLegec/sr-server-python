from flask import Flask, jsonify, session, request
from flask_restful import Api
from flask_socketio import SocketIO, join_room
from flask_cors import CORS

from files import DirectoryController
from files import FileController
from resources import Files
from resources import Records
from clients import ClientController

app = Flask('File Server')
CORS(app)
app.config['SECRET_KEY'] = 'Secret!!!'
socketio = SocketIO(app)
clients_controller = ClientController(socketio)
dir_controller = DirectoryController(clients_controller)
file_controller = FileController(dir_controller, clients_controller)
api = Api(app)
api.add_resource(
    Files,
    '/files', '/files/<string:name>',
    resource_class_kwargs={'directory_controller': dir_controller}
)
api.add_resource(
    Records,
    '/files/<string:name>/records', '/files/<string:name>/records/<int:record_id>',
    resource_class_kwargs={'file_controller': file_controller}
)


@app.route('/health')
def health_check():
    return jsonify('OK')


@socketio.on('connect')
def connect_handler():
    sid = request.sid
    clients_controller.register_client(sid)
    print("New user connected")


@socketio.on('disconnect')
def disconnect_handler():
    sid = request.sid
    clients_controller.remove_client(sid)
    print("User disconnected")


@socketio.on('authorize')
def authorize_handler(json):
    login = json['userId']
    sid = request.sid
    join_room(login)
    clients_controller.set_login_for_client(sid, login)
    print("User authorized: " + login)


@socketio.on('file_state_change')
def file_event_handler(json):
    event_type = json['eventType']
    filename = json['file']
    username = json['userId']
    print("Event: " + event_type + " for file: " + filename + " send by: " + username)
    if event_type == "OPEN_FILE":
        dir_controller.add_opened_by(filename, username)
    elif event_type == "CLOSE_FILE":
        dir_controller.remove_opened_by(filename, username)
    else:
        raise ValueError("Invalid eventType")


@socketio.on('record_state_change')
def record_event_handler(json):
    event_type = json['eventType']
    file_name = json['file']
    record_id = json['record']
    username = json['userId']
    print("Event: " + event_type + " for record #" + str(record_id) + " in file: " + file_name + " by user: " + username)


def start(host='0.0.0.0', port=4200, debug=False):
    socketio.run(app, host, port, debug=debug)


if __name__ == '__main__':
    start(debug=True)
