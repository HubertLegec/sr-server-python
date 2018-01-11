from threading import Thread
import requests
import uuid

from urllib3.exceptions import HTTPError

from server.deadlocks import DeadlockDetector, SnapshotDescription
from server.utils import LogFactory, RepeatedTimer

log = LogFactory.get_logger()


class DeadlockController:
    def __init__(self, file_controller, snapshot_builder, servers, interval=10):
        self.__main_thread = RepeatedTimer(interval, DeadlockController.check_deadlocks, snapshot_builder, servers, file_controller)

    def run(self):
        log.info('Run deadlock detector...')
        self.__main_thread.start()

    @staticmethod
    def check_deadlocks(snapshot_builder, servers, file_controller):
        log.info('Check deadlocks...')
        snapshot_uuid = str(uuid.uuid4())
        detector = DeadlockDetector(snapshot_uuid)
        own_snapshot = snapshot_builder.create_snapshot(snapshot_uuid)
        own_server = {'host': None, 'port': None}
        detector.add_snapshot(SnapshotDescription(own_snapshot, own_server))
        threads = [Thread(target=DeadlockController.get_snapshot_for_server, args=(s, detector, snapshot_uuid)) for s in servers]
        DeadlockController.run_threads_for_result(threads)
        detector.build_graph()
        removed = detector.get_cycle_and_remove()
        while removed is not None:
            if removed.server_host is None and removed.server_port is None:
                log.info("Removing waiting user: " + removed.waiting_user + ' on this server...')
                file_controller.remove_user_from_queue(removed.filename, removed.record_id, removed.waiting_user, removed.timestamp)
            else:
                DeadlockController.remove_waiting_client(removed)
            removed = detector.get_cycle_and_remove()

    @staticmethod
    def get_snapshot_for_server(server, detector, id):
        server_address = server['host'] + ':' + str(server['port'])
        log.info('Get snapshot ' + id + ' for server: ' + server_address)
        url = 'http://' + server_address + '/snapshots/' + id
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                log.info('Snapshot fetched from server ' + server_address)
                detector.add_snapshot(SnapshotDescription(resp.json(), server))
            else:
                log.error('Error occurred during fetching snapshot from server: ' + server_address)
        except (OSError, HTTPError):
            log.error('Error occurred during fetching snapshot from server: ' + server_address)

    @staticmethod
    def run_threads_for_result(threads):
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    @staticmethod
    def remove_waiting_client(to_remove):
        log.info("Remove waiting request for user: " + to_remove.waiting_user)
        url = 'http://' + to_remove.server_host + ':' + str(to_remove.server_port) + '/files/' \
              + to_remove.filename + '/records/' + str(to_remove.record_id) + '/clients?' \
              + 'client_id=' + to_remove.waiting_user + '&timestamp=' + to_remove.timestamp
        resp = requests.delete(url)
        if resp.status_code == 200:
            log.info("Waiting user removed successfully")
        else:
            log.error("Error occurred during removing waiting user, url: " + url)
