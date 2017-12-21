
class FileController:
    def __init__(self, directory_controller):
        self.directory_controller = directory_controller

    def get_records(self, filename):
        file = self.directory_controller.get_file(filename)
        return file.get_records()

    def create_record(self, filename, content):
        file = self.directory_controller.get_file(filename)
        return file.create_record(content)

    def update_record(self, filename, record_id, content):
        file = self.directory_controller.get_file(filename)
        record = file.get_record(record_id)
        record.set_content(content)

    def delete_record(self, filename, record_id):
        file = self.directory_controller.get_file(filename)
        file.delete_record(record_id)