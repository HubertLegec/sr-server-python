from server.files import SystemFilesController
from server.utils import LogFactory
from . import File


class DirectoryController:
    log = LogFactory.get_logger()

    def __init__(self, clients_controller, dir_name):
        self.__system_files_controller = SystemFilesController(dir_name)
        self.__clients_controller = clients_controller
        self.__files = self.__system_files_controller.get_all_files()

    def get_files(self):
        return self.__files

    def get_file(self, name):
        filtered = [f for f in self.__files if f.get_name() == name]
        if len(filtered) == 0:
            raise FileNotFoundError("File with name " + name + " doesn't exist")
        return filtered[0]

    def create_file(self, name):
        self.log.info('Creating file with name: ' + name)
        name_exists = self.__check_if_name_exists(name)
        if name_exists:
            raise FileExistsError("File with name " + name + " already exists")
        file = File(name)
        self.__files.append(file)
        self.__system_files_controller.create_file(name)
        self.log.info('File with name: ' + name + ' created')
        return file

    def delete_file(self, name):
        self.log.info('Deleting file with name: ' + name)
        file = self.get_file(name)
        if len(file.get_opened_by()) > 0:
            msg = "Can't remove file " + name + ", it's opened by at least one client"
            self.log.error("Can't remove file " + name + ", it's opened by at least one client")
            raise PermissionError(msg)
        self.__files = [f for f in self.__files if f.get_name() != name]
        self.__system_files_controller.delete_file(name)
        self.log.info('File with name: ' + name + ' deleted')
        return None

    def add_opened_by(self, name, user):
        file = self.get_file(name)
        return file.add_opened_by(user)

    def remove_opened_by(self, name, user):
        file = self.get_file(name)
        file.remove_opened_by(user)

    def disconnect_user(self, user_id):
        self.log.info("Disconnecting client from all files...")
        for f in self.get_files():
            to_notify = f.disconnect_user(user_id)
            for entry in to_notify:
                self.__notify_specified_client(
                    entry[1],
                    {'eventType': 'LOCK_ASSIGNED', 'recordId': entry[0], 'filename': f.get_name()}
                )

    def get_system_files_controller(self):
        return self.__system_files_controller

    def __check_if_name_exists(self, name):
        filtered = [f for f in self.__files if f.get_name() == name]
        return len(filtered) > 0

    def __notify_specified_client(self, user, body):
        self.__clients_controller.emit(
            [user],
            'record_state_change',
            body
        )
