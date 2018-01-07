from server.utils import LogFactory


class SnapshotBuilder:
    def __init__(self, dir_controller):
        self.log = LogFactory.get_logger()
        self.dir_controller = dir_controller

    def create_snapshot(self, snapshot_id):
        self.log.info('Create snapshot #' + str(snapshot_id) + '...')
        files = self.dir_controller.get_files()
        return {f.get_name(): self.__create_file_snapshot(f) for f in files}

    @classmethod
    def __create_file_snapshot(cls, file):
        records = file.get_records()
        return {r.get_id(): cls.__create_record_snapshot(r) for r in records}

    @classmethod
    def __create_record_snapshot(cls, record):
        return {
            'lockedBy': record.get_locked_by(),
            'waiting': [u.to_dictionary() for u in record.get_waiting_users()]
        }