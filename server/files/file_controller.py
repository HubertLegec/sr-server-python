
class FileController:
    def __init__(self, directory_controller, clients_controller):
        self.directory_controller = directory_controller
        self.__clients_controller = clients_controller

    def get_records(self, filename):
        file = self.directory_controller.get_file(filename)
        return file.get_records()

    def create_record(self, filename, content):
        file = self.directory_controller.get_file(filename)
        new_record_id = file.create_record(content)
        opened_by = file.get_opened_by()
        self.__clients_controller.emit(
            opened_by, 'recordCreated', {'recordId': new_record_id, 'filename': file.get_name()}
        )
        return new_record_id

    def update_record(self, filename, record_id, content):
        file = self.directory_controller.get_file(filename)
        record = file.get_record(record_id)
        record.set_content(content)

    def delete_record(self, filename, record_id):
        file = self.directory_controller.get_file(filename)
        file.delete_record(record_id)
        opened_by = file.get_opened_by()
        self.__clients_controller.emit(
            opened_by, 'recordRemoved', {'recordId': record_id, 'filename': file.get_name()}
        )
