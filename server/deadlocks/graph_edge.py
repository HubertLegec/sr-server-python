
class GraphEdge:
    def __init__(self, waiting_user, locking_user, filename, record_id, snapshot_descr):
        self.locking_user = locking_user
        self.waiting_user = waiting_user['userId']
        self.timestamp = waiting_user['timestamp']
        self.filename = filename
        self.record_id = record_id if isinstance(record_id, int) else int(record_id)
        self.server_host = snapshot_descr.get_host()
        self.server_port = snapshot_descr.get_port()
