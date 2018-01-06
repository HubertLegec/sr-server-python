from flask_restful import Resource
from flask import jsonify, request

from server.snapshots import SnapshotRequest


class Snapshots(Resource):
    def __init__(self, **kwargs):
        self.__snapshot_controller = kwargs['snapshot_controller']

    def get(self, snapshot_id):
        req = SnapshotRequest(request.host, snapshot_id)
        self.__snapshot_controller.requests_queue.put(req)
        response = jsonify({
            'message': 'Request accepted'
        })
        response.status_code = 202
        return response

    def post(self, snapshot_id):
        body_json = request.get_json()

        return None
