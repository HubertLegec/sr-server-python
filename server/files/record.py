import sys
from queue import Queue


class Record:
    MAX_RECORD_SIZE = 1024

    def __init__(self, id):
        self.__id = id
        self.__content = ""
        self.__locked_by = None
        self.__lock_queue = Queue()

    def get_content(self):
        return self.__content

    def get_id(self):
        return self.__id

    def get_locked_by(self):
        return self.__locked_by

    def set_content(self, content):
        size = sys.getsizeof(content)
        if size > Record.MAX_RECORD_SIZE:
            raise ValueError("Can't set new value of record #" + str(self.__id) + ", max size exceeded")
        self.__content = content

    def lock(self, user_id):
        if self.__locked_by is None:
            self.__locked_by = user_id
            return True
        else:
            self.__lock_queue.put(user_id)
            return False

    # TODO - improve operation atomicity
    def unlock(self, user_id):
        if self.__locked_by == user_id:
            if self.__lock_queue.empty():
                self.__locked_by = None
            else:
                next_user = self.__lock_queue.get()
                self.__locked_by = next_user
            return self.__locked_by
        else:
            raise PermissionError('Unlock not allowed, user ' + user_id + ' has no rights to record')

    def get_waiting_users(self):
        return [u for u in self.__lock_queue.queue]

