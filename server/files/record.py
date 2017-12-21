import sys


class Record:
    MAX_RECORD_SIZE = 1024

    def __init__(self, id):
        self.__id = id
        self.__content = ""

    def get_content(self):
        return self.__content

    def get_id(self):
        return self.__id

    def set_content(self, content):
        size = sys.getsizeof(content)
        if size > Record.MAX_RECORD_SIZE:
            raise ValueError("Can't set new value of record #" + str(self.__id) + ", max size exceeded")
        self.__content = content

