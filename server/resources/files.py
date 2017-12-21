from flask_restful import Resource


class Files(Resource):
    def __init__(self, **kwargs):
        self.directory_controller = kwargs['directory_controller']

    def get(self):
        return self.directory_controller.get_files_list()

    def post(self):
        name = 'file1'
        self.directory_controller.create_file(name)
        return 'OK'

    def delete(self, name):
        self.directory_controller.delete_file(name)
        return 'OK'
