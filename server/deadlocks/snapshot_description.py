
class SnapshotDescription:
    def __init__(self, snapshot, server):
        self.__snapshot_data = snapshot
        self.__host = server['host']
        self.__port = server['port']

    def get_data(self):
        return self.__snapshot_data

    def get_host(self):
        return self.__host

    def get_port(self):
        return self.__port
