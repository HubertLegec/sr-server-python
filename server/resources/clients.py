from flask_restful import Resource
from flask import request, jsonify


class Clients(Resource):
    def __init__(self, **kwargs):
        self.__file_controller = kwargs['file_controller']

    def delete(self, name, record_id):
        client_id = request.args.get('client_id')
        timestamp = request.args.get('timestamp')
        result = self.__file_controller.remove_user_from_queue(name, record_id, client_id, timestamp)
        if result:
            return jsonify({
                'message': 'User #' + client_id + ' removed from queue'
            })
        else:
            return jsonify({
                'message': 'User #' + client_id + ' is not present in queue or has been already removed'
            })
