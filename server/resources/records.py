from flask_restful import Resource
from flask import jsonify, request


class Records(Resource):
    def __init__(self, **kwargs):
        self.file_controller = kwargs['file_controller']

    def get(self, name):
        records = self.file_controller.get_records(name)
        mapped_records = [{'id': r.get_id(), 'content': r.get_content()} for r in records]
        return jsonify(mapped_records)

    def post(self, name):
        req_body = request.get_json()
        user_id = request.headers['userId']
        content = req_body['content']
        rec_id = self.file_controller.create_record(name, content, user_id)
        return jsonify({
            'message': 'Record created',
            'recordId': rec_id
        })

    def put(self, name, record_id):
        req_body = request.get_json()
        user_id = request.headers['userId']
        content = req_body['content']
        self.file_controller.update_record(name, record_id, content, user_id)
        return jsonify({
            'message': 'Record #%d in file %s updated' % (record_id, name)
        })

    def delete(self, name, record_id):
        user_id = request.headers['userId']
        self.file_controller.delete_record(name, record_id, user_id)
        return jsonify({
            'message': 'Record #%d in file %s removed' % (record_id, name)
        })

