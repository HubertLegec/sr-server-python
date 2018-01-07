from flask_restful import Resource
from flask import jsonify


class Snapshots(Resource):
    def __init__(self, **kwargs):
        self.__snapshot_builder = kwargs['snapshot_builder']

    def get(self, snapshot_id):
        snapshot = self.__snapshot_builder.create_snapshot(snapshot_id)
        return jsonify(snapshot)
