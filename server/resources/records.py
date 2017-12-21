from flask_restful import Resource


class Records(Resource):
    def __init__(self, **kwargs):
        self.file_controller = kwargs['file_controller']

    def get(self, name):
        return None

    def post(self, name):
        return None

    def put(self, name, record_id):
        return None

    def delete(self, name, record_id):
        return None

