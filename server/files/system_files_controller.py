from os import path, makedirs, remove, listdir

from server.files import File, Record
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
        return [self.__restore_file(n) for n in names]

    def create_record(self, filename, record):
        with open(self.__create_file_path(filename), "a") as f:
            f.write(str(record.get_id()) + ":" + record.get_content() + "\n")

    def __restore_file(self, filename):
        self.log.info('Restore file: ' + filename)
        file = File(filename)
        with open(self.__create_file_path(filename)) as f:
            content = f.readlines()
            records = [self.__restore_record(r.strip()) for r in content]
            file.set_records(records)
        return file

    @classmethod
    def __restore_record(cls, line):
        semicolon_idx = line.index(":")
        rec_id = int(line[0:semicolon_idx])
        rec_content = line[semicolon_idx+1:]
        rec = Record(rec_id)
        rec.set_content(rec_content)
        return rec

    def __create_file_path(self, filename):
        return path.join(self.__dir_path, filename)
