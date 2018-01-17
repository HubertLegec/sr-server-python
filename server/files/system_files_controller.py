from os import path, makedirs, remove, listdir

from server.files import File
from server.utils import LogFactory


class SystemFilesController:
    log = LogFactory.get_logger()

    def __init__(self, dir_path):
        self.__dir_path = dir_path
        self.ensure_dir_exists()

    def ensure_dir_exists(self):
        if not path.isdir(self.__dir_path):
            self.log.info('Create files dir: ' + self.__dir_path)
            makedirs(self.__dir_path)
        else:
            self.log.info('Files directory already exists: ' + self.__dir_path)

    def create_file(self, filename):
        file_path = self.__create_file_path(filename)
        file = open(file_path, "w")
        file.close()

    def delete_file(self, filename):
        remove(self.__create_file_path(filename))

    def get_all_files(self):
        names = [f for f in listdir(self.__dir_path) if path.isfile(self.__create_file_path(f))]
        return [File(n) for n in names]

    def __create_file_path(self, filename):
        return path.join(self.__dir_path, filename)
