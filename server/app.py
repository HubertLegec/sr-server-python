from flask import Flask, jsonify
from flask_restful import Api
from flask_socketio import SocketIO
from flask_cors import CORS

from server.deadlocks import DeadlockController
from server.files import DirectoryController
from server.files import FileController
from server.resources import Files
from server.resources import Records
from server.resources import Snapshots
from server.resources import Clients
from server.resources import WebsocketNamespace
from server.snapshots import SnapshotBuilder
from server.clients import ClientController
from server.utils import LogFactory, ConfigLoader

app_configured = False
app = Flask('File Server')
CORS(app)
app.config['SECRET_KEY'] = 'Secret!!!'
app.config['TRAP_HTTP_EXCEPTIONS'] = True
socketio = SocketIO(app, async_mode='eventlet')
logger = LogFactory.get_logger()


def handle_permission_error(error):
    response = jsonify({
        'message': str(error)
    })
    response.status_code = 403
    return response


def handle_not_found_error(error):
    response = jsonify({
        'message': str(error)
    })
    response.status_code = 404
    return response


def handle_exist_error(error):
    response = jsonify({
        'message': str(error)
    })
    response.status_code = 409
    return response


def configure(configuration):
    global app, app_configured, socketio
    if app_configured:
        return app, socketio
    clients_controller = ClientController(socketio)
    dir_controller = DirectoryController(clients_controller, configuration.get_files_dir())
    file_controller = FileController(dir_controller, clients_controller)
    snapshot_builder = SnapshotBuilder(dir_controller)
    deadlock_controller = DeadlockController(file_controller, snapshot_builder, configuration)
    handle_exception = app.handle_exception
    handle_user_exception = app.handle_user_exception
    api = Api(app)
    app.handle_exception = handle_exception
    app.handle_user_exception = handle_user_exception
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
    api.add_resource(
        Snapshots,
        '/snapshots/<string:snapshot_id>',
        resource_class_kwargs={'snapshot_builder': snapshot_builder}
    )
    api.add_resource(
        Clients,
        '/files/<string:name>/records/<int:record_id>/clients',
        resource_class_kwargs={'file_controller': file_controller}
    )
    app.register_error_handler(PermissionError, handle_permission_error)
    app.register_error_handler(FileNotFoundError, handle_not_found_error)
    app.register_error_handler(FileExistsError, handle_exist_error)
    socketio.on_namespace(WebsocketNamespace(clients_controller, dir_controller, file_controller))
    app_configured = True
    return app, socketio, deadlock_controller


def start(params):
    configuration = ConfigLoader(params.config, params.server)
    host = configuration.get_server_host()
    port = configuration.get_server_port()
    debug = params.debug
    app, socketio, deadlock_controller = configure(configuration)
    deadlock_controller.run()
    socketio.run(app, host, port, debug=debug)
