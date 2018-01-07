import sys
from server.utils import Queue

from . import WaitingClient


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
        return self.__locked_by.get_user() if self.__locked_by else None

    def set_content(self, content):
        size = sys.getsizeof(content)
        if size > Record.MAX_RECORD_SIZE:
            raise ValueError("Can't set new value of record #" + str(self.__id) + ", max size exceeded")
        self.__content = content

    def lock(self, user_id):
        if self.__locked_by is None:
            self.__locked_by = WaitingClient(user_id)
            return True
        else:
            self.__lock_queue.put(user_id)
            return False

    def unlock(self, user_id):
        if self.__locked_by and self.__locked_by.get_user() == user_id:
            next_user = self.__lock_queue.pop()
            self.__locked_by = next_user
            return next_user
        else:
            raise PermissionError('Unlock not allowed, user ' + user_id + ' has no rights to record')

    def remove_waiting_user(self, user_id, timestamp):
        return self.__lock_queue.remove_by(lambda u: u.get_user() == user_id and u.get_timestamp() == timestamp)

    def get_waiting_users(self):
        return [u for u in self.__lock_queue.get_as_list()]

