
class SnapshotRequest:
    def __init__(self, request_host, snapshot_id):
        self.__id = snapshot_id
        self.__host = request_host

    def get_id(self):
        return self.__id

    def get_host(self):
        return self.__host
