import requests
from queue import Queue
from threading import Thread

from server.utils import LogFactory
from . import SnapshotBuilder


class SnapshotController:

    def __init__(self, dir_controller, servers):
        self.log = LogFactory.get_logger()
        self.snapshot_builder = SnapshotBuilder(dir_controller)
        self.servers = servers
        self.requests_queue = Queue()
        self.snapshot_creator_worker = Thread(
            target=SnapshotController.process_requests,
            args=(self.snapshot_builder, self.requests_queue)
        )
        self.snapshot_creator_worker.setDaemon(True)

    def start(self):
        self.log.info('Start snapshot controller')
        self.snapshot_creator_worker.start()

    @staticmethod
    def process_requests(snapshot_builder, queue):
        log = LogFactory.get_logger()
        while True:
            log.info('Waiting for snapshot request...')
            request = queue.get()
            snapshot_id = request.get_id()
            log.info('New snapshot request #' + str(snapshot_id))
            snapshot = snapshot_builder.create_snapshot()
            log.info('Snapshot #' + str(snapshot_id) + ' ready.')
            url = 'http://' + request.get_host() + '/snapshots/' + str(request.get_id())
            resp = requests.post(url, data=snapshot)
            if resp.status_code == 200:
                log.info('Snapshot #' + str(snapshot_id) + ' send back')
            else:
                log.error('Error during posting snapshot #' + snapshot_id + ' on url: ' + url + ', response: ' + str(resp.status_code) + ' ' + resp.reason)


