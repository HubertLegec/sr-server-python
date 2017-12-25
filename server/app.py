from flask import Flask, jsonify
from flask_restful import Api
from flask_socketio import SocketIO
from flask_cors import CORS

from files import DirectoryController
from files import FileController
from resources import Files
from resources import Records

app = Flask('File Server')
CORS(app)
app.config['SECRET_KEY'] = 'Secret!!!'
dir_controller = DirectoryController()
file_controller = FileController(dir_controller)
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
socketio = SocketIO(app)


@app.route('/health')
def health_check():
    return jsonify('OK')


@socketio.on('connect')
def connect_handler():
    print("New user connected")


@socketio.on('disconnect')
def disconnect_handler():
    print("User disconnected")


@socketio.on('authorize')
def authorize_handler(json):
    login = json['userId']
    print("User authorized")


def start(host='0.0.0.0', port=4200, debug=False):
    socketio.run(app, host, port, debug=debug)


if __name__ == '__main__':
    start(debug=True)
