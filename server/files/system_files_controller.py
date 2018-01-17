from os import path, makedirs, remove, listdir

from server.files import File, Record
from server.utils import LogFactory


class SystemFilesController:
    log = LogFactory.get_logger()
    empty_record = " " * 1024

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
        with open(self.__create_file_path(filename), "r+b") as f:
            f.seek(record.get_id() * 1024)
            f.write(self.empty_record.encode())
            f.seek(record.get_id() * 1024)
            f.write(record.get_content().encode())

    def delete_record(self, filename, record_id):
        with open(self.__create_file_path(filename), "r+b") as f:
            f.seek(record_id * 1024)
            f.write(self.empty_record.encode())

    def update_record(self, filename, record_id, content):
        with open(self.__create_file_path(filename), "r+b") as f:
            f.seek(record_id * 1024)
            f.write(self.empty_record.encode())
            f.seek(record_id * 1024)
            f.write(content.encode())

    def __restore_file(self, filename):
        self.log.info('Restore file: ' + filename)
        file = File(filename)
        rec_idx = 0
        records = []
        with open(self.__create_file_path(filename), "r+b") as f:
            bytes_read = f.read(1024)
            while bytes_read:
                bytes_str = bytes_read.decode()
                if not bytes_str.isspace():
                    rec = Record(rec_idx)
                    rec.set_content(bytes_str.strip())
                    records.append(rec)
                rec_idx += 1
                bytes_read = f.read(1024)
            file.set_records(records)
        return file

    def __create_file_path(self, filename):
        return path.join(self.__dir_path, filename)
