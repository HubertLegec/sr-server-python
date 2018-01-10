from threading import Thread
import requests
import uuid

from urllib3.exceptions import HTTPError

from server.deadlocks import DeadlockDetector
from server.utils import LogFactory, RepeatedTimer

log = LogFactory.get_logger()


class DeadlockController:
    def __init__(self, snapshot_builder, servers, interval=10):
        self.__main_thread = RepeatedTimer(interval, DeadlockController.check_deadlocks, snapshot_builder, servers)

    def run(self):
        log.info('Run deadlock detector...')
        self.__main_thread.start()

    @staticmethod
    def check_deadlocks(snapshot_builder, servers):
        log.info('Check deadlocks...')
        detector = DeadlockDetector()
        snapshot_uuid = str(uuid.uuid4())
        own_snapshot = snapshot_builder.create_snapshot(snapshot_uuid)
        detector.add_snapshot(own_snapshot)
        threads = [Thread(target=DeadlockController.get_snapshot_for_server, args=(s, detector, snapshot_uuid)) for s in servers]
        DeadlockController.run_threads_for_result(threads)
        cycle = detector.get_cycle()
        if cycle is not None:
            log.info('Cycle found !!!')
        None

    @staticmethod
    def get_snapshot_for_server(server, detector, id):
        server_address = server['host'] + ':' + str(server['port'])
        log.info('Get snapshot ' + id + ' for server: ' + server_address)
        url = 'http://' + server_address + '/snapshots/' + id
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                log.info('Snapshot fetched from server ' + server_address)
                detector.add_snapshot(resp.json())
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
