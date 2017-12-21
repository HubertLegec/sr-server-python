from . import Record


class File:
    def __init__(self, name):
        self.__name = name
        self.__records = []

    def get_name(self):
        return self.__name

    def get_records(self):
        return self.__records

    def get_record(self, record_id):
        filtered = [r for r in self.__records if r.get_id() == record_id]
        if len(filtered) == 0:
            raise RuntimeError("Record #" + str(record_id) + " not found")
        return filtered[0]

    def delete_record(self, record_id):
        self.__records = [r for r in self.__records if r.get_id() != record_id]

    def create_record(self, content):
        rec_id = self.__get_next_record_id()
        record = Record(rec_id)
        record.set_content(content)
        self.__records.append(record)
        return rec_id

    def __get_next_record_id(self):
        if len(self.__records) == 0:
            return 0
        return max(map(lambda x: x.get_id(), self.__records)) + 1
