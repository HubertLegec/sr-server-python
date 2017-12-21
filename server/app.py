from flask import Flask, jsonify, request
from flask_restful import Api

from files import DirectoryController
from files import FileController
from resources import Files
from resources import Records

app = Flask('File Server')
app_configured = False
NOT_FOUND_CODE = 404


@app.errorhandler(FileNotFoundError)
def not_found_error(error):
    return jsonify(request.url + ' not found'), NOT_FOUND_CODE


@app.route('/health')
def health_check():
    return jsonify('OK')


def configure(config):
    global app_configured
    global app
    if not app_configured:
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
        app_configured = True
    return app


def start(config, host='0.0.0.0', port=3000, debug=False):
    application = configure(config)
    application.run(host, port, debug)


if __name__ == '__main__':
    config = {}
    start(config, debug=True)
