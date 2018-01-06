from server.utils import LogFactory
from . import Record


class File:
    log = LogFactory.get_logger()

    def __init__(self, name):
        self.__name = name
        self.__records = []
        self.__opened_by = []

    def get_name(self):
        return self.__name

    def get_records(self):
        return self.__records

    def get_record(self, record_id):
        filtered = [r for r in self.__records if r.get_id() == record_id]
        if len(filtered) == 0:
            raise FileNotFoundError("Record #" + str(record_id) + " not found")
        return filtered[0]

    def delete_record(self, record_id, user_id):
        record = self.get_record(record_id)
        locked_by = record.get_locked_by()
        if locked_by == user_id:
            self.__records = [r for r in self.__records if r.get_id() != record_id]
        else:
            msg = "Delete not allowed, user " + user_id + " has no rights for record"
            self.log.error(msg)
            raise PermissionError(msg)

    def create_record(self, content):
        rec_id = self.__get_next_record_id()
        record = Record(rec_id)
        record.set_content(content)
        self.__records.append(record)
        return record

    def edit_record(self, record_id, content, user_id):
        record = self.get_record(record_id)
        locked_by = record.get_locked_by()
        if locked_by == user_id:
            record.set_content(content)
        else:
            msg = "Edit not allowed, user " + user_id + " has no rights for record"
            self.log.error(msg)
            raise PermissionError(msg)

    def add_opened_by(self, user):
        if user not in self.__opened_by:
            self.__opened_by.append(user)
            return True
        return False

    def get_opened_by(self):
        return self.__opened_by

    def remove_opened_by(self, user):
        self.__opened_by = [o for o in self.__opened_by if o != user]

    def lock_record(self, user, record_id):
        self.log.info("Lock record #" + str(record_id) + " for user: " + user)
        record = self.get_record(record_id)
        return record.lock(user)

    def unlock_record(self, user, record_id):
        self.log.info("Unlock record #" + str(record_id) + " locked by: " + user)
        record = self.get_record(record_id)
        return record.unlock(user)

    def __get_next_record_id(self):
        if len(self.__records) == 0:
            return 0
        return max(map(lambda x: x.get_id(), self.__records)) + 1
