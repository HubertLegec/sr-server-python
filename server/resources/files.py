from flask_restful import Resource
from flask import jsonify, request


class Files(Resource):
    def __init__(self, **kwargs):
        self.directory_controller = kwargs['directory_controller']

    def get(self):
        files_list = self.directory_controller.get_files()
        names = [f.get_name() for f in files_list]
        return jsonify(names)

    def post(self):
        request_body = request.get_json()
        name = request_body['filename']
        self.directory_controller.create_file(name)
        return jsonify({
            'message': ('File with name ' + name + ' created.')
        })

    def delete(self, name):
        self.directory_controller.delete_file(name)
        return jsonify({
            'message': 'File with name ' + name + ' removed.'
        })
