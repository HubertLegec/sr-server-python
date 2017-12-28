class FileController:
    def __init__(self, directory_controller, clients_controller):
        self.directory_controller = directory_controller
        self.__clients_controller = clients_controller

    def get_records(self, filename):
        file = self.directory_controller.get_file(filename)
        return file.get_records()

    def create_record(self, filename, content, user_id):
        file = self.directory_controller.get_file(filename)
        new_record = file.create_record(content)
        self.__notify_clients(
            file, user_id,
            {
                'eventType': 'RECORD_CREATED',
                'record': {
                    'id': new_record.get_id(),
                    'content': new_record.get_content(),
                    'filename': file.get_name()
                }
            }
        )
        return new_record.get_id()

    def update_record(self, filename, record_id, content, user_id):
        file = self.directory_controller.get_file(filename)
        record = file.get_record(record_id)
        record.set_content(content)
        self.__notify_clients(
            file, user_id, {'eventType': 'RECORD_UPDATED', 'recordId': record_id, filename: file.get_name()}
        )

    def delete_record(self, filename, record_id, user_id):
        file = self.directory_controller.get_file(filename)
        file.delete_record(record_id)
        self.__notify_clients(
            file, user_id, {'eventType': 'RECORD_REMOVED', 'recordId': record_id, 'filename': file.get_name()}
        )

    def __notify_clients(self, file, current_user, body):
        opened_by = [c for c in file.get_opened_by() if c != current_user]
        self.__clients_controller.emit(
            opened_by,
            'record_state_change',
            body
        )
