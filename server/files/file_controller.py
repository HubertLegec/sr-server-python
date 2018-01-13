from server.utils import LogFactory
from dateutil import parser


class FileController:
    log = LogFactory.get_logger()

    def __init__(self, directory_controller, clients_controller):
        self.directory_controller = directory_controller
        self.__clients_controller = clients_controller

    def get_records(self, filename):
        file = self.directory_controller.get_file(filename)
        return file.get_records()

    def create_record(self, filename, content, user_id):
        self.log.info('Creating record in file: ' + filename + ' by user: ' + user_id)
        file = self.directory_controller.get_file(filename)
        if len(file.get_records()) >= 1024:
            raise Exception("Max file size (1024 records) exceeded!")
        new_record = file.create_record(content)
        self.log.info('New record #' + str(new_record.get_id()) + ' created in file: ' + filename + ' by user: ' + user_id)
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
        self.log.info('Updating record #' + str(record_id) + ' in file: ' + filename + ' by user: ' + user_id)
        file = self.directory_controller.get_file(filename)
        file.edit_record(record_id, content, user_id)
        self.log.info('Record #' + str(record_id) + ' in file: ' + filename + ' updated by user: ' + user_id)
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
        self.log.info('Deleting record #' + str(record_id) + ' in file: ' + filename + ' by user: ' + user_id)
        file = self.directory_controller.get_file(filename)
        file.delete_record(record_id, user_id)
        self.log.info('Record #' + str(record_id) + ' in file: ' + filename + ' deleted by user: ' + user_id)
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

    def remove_user_from_queue(self, filename, record_id, user_id, timestamp):
        self.log.info('Removing user: ' + user_id + ' who locked record #' + str(record_id) + ' in file: ' + filename)
        assert isinstance(filename, str)
        assert isinstance(record_id, int)
        assert isinstance(user_id, str)
        file = self.directory_controller.get_file(filename)
        record = file.get_record(record_id)
        user_removed = record.remove_waiting_user(user_id, parser.parse(timestamp))
        if user_removed:
            self.log.info('User: ' + user_id + ' removed from record #' + str(record_id) + ' in file: ' + filename)
            self.__notify_specified_client(
                user_id,
                {'eventType': 'LOCK_REJECTED', 'recordId': record_id, 'filename': filename}
            )
        else:
            self.log.warn('User: ' + user_id + ' not removed from record #' + str(record_id) + ' in file: ' + filename)
        return user_removed

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
