from flask_restful import Resource
from flask import jsonify, request


class Records(Resource):
    def __init__(self, **kwargs):
        self.file_controller = kwargs['file_controller']

    def get(self, name):
        records = self.file_controller.get_records(name)
        user_id = request.headers['userId']
        mapped_records = [Records.__record_to_json(r, user_id, name) for r in records]
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
        user_id = request.headers['userId']
        req_body = request.get_json()
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

    @staticmethod
    def __record_to_json(record, user_id, filename):
        locked_by = record.get_locked_by()
        state = 'EDITING' if locked_by == user_id else 'AVAILABLE'  # TODO waiting status
        return {'id': record.get_id(), 'content': record.get_content(), 'status': state, 'filename': filename}
