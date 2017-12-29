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
                    'filename': filename
                }
            }
        )
        return new_record.get_id()

    def update_record(self, filename, record_id, content, user_id):
        file = self.directory_controller.get_file(filename)
        file.edit_record(record_id, content, user_id)
        self.__notify_clients(
            file, user_id,
            {
                'eventType': 'RECORD_UPDATED',
                'record': {
                    'id': record_id,
                    'content': content,
                    'filename': filename
                }
            }
        )

    def delete_record(self, filename, record_id, user_id):
        file = self.directory_controller.get_file(filename)
        file.delete_record(record_id, user_id)
        self.__notify_clients(
            file, user_id, {'eventType': 'RECORD_REMOVED', 'recordId': record_id, 'filename': filename}
        )

    def lock_record(self, filename, record_id, user_id):
        file = self.directory_controller.get_file(filename)
        lock_result = file.lock_record(user_id, record_id)
        if lock_result:
            self.__notify_specified_client(
                user_id, {'eventType': 'LOCK_ASSIGNED', 'recordId': record_id, 'filename': filename}
            )
            # self.__notify_clients(
            #     file, user_id, {'eventType': 'RECORD_LOCKED', 'recordId': record_id, 'filename': filename}
            # )
        return lock_result

    def unlock_record(self, filename, record_id, user_id):
        file = self.directory_controller.get_file(filename)
        next_user = file.unlock_record(user_id, record_id)
        self.__notify_specified_client(
            user_id, {'eventType': 'LOCK_PICKED_UP', 'recordId': record_id, 'filename': filename}
        )
        if next_user is not None:
            self.__notify_specified_client(
                next_user,
                {'eventType': 'LOCK_ASSIGNED', 'recordId': record_id, 'filename': filename}
            )
        # else:
        #     self.__notify_clients(
        #         file, user_id, {'eventType': 'RECORD_UNLOCKED', 'recordId': record_id, 'filename': filename}
        #     )

    def __notify_clients(self, file, current_user, body):
        opened_by = [c for c in file.get_opened_by() if c != current_user]
        self.__clients_controller.emit(
            opened_by,
            'record_state_change',
            body
        )

    def __notify_specified_client(self, user, body):
        self.__clients_controller.emit(
            [user],
            'record_state_change',
            body
        )
