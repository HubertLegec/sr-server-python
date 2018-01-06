from server.utils import LogFactory
from . import File


class DirectoryController:
    log = LogFactory.get_logger()

    def __init__(self, clients_controller):
        self.__files = []
        self.__clients_controller = clients_controller

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
        self.log.info('File with name: ' + name + ' deleted')
        return None

    def add_opened_by(self, name, user):
        file = self.get_file(name)
        return file.add_opened_by(user)

    def remove_opened_by(self, name, user):
        file = self.get_file(name)
        file.remove_opened_by(user)

    def __check_if_name_exists(self, name):
        filtered = [f for f in self.__files if f.get_name() == name]
        return len(filtered) > 0
