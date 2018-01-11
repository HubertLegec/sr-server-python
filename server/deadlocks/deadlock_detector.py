from server.deadlocks import GraphEdge, WaitForGraph
from server.utils import LogFactory


class DeadlockDetector:
    log = LogFactory.get_logger()

    def __init__(self, snapshot_id):
        self.__snapshot_id = snapshot_id
        self.__snapshots = []
        self.__graph = None

    def add_snapshot(self, snapshot):
        self.__snapshots.append(snapshot)

    def build_graph(self):
        self.__graph = self.build_wait_for_graph(self.__snapshots)

    def get_cycle_and_remove(self):
        cycle_path = self.__graph.find_cycle()
        if cycle_path:
            self.log.info('Cycle found in snapshot #' + self.__snapshot_id + "!")
            youngest_edge = WaitForGraph.get_youngest_edge(cycle_path)
            self.__graph.remove_edge(youngest_edge)
            return youngest_edge
        return None

    @staticmethod
    def build_wait_for_graph(snapshots):
        graph = WaitForGraph()
        for snapshot in snapshots:
            snapshot_data = snapshot.get_data()
            files = snapshot_data.keys()
            for filename in files:
                file = snapshot_data[filename]
                records = file.keys()
                for record_id in records:
                    record = file[record_id]
                    locked_by = record['lockedBy']
                    if locked_by:
                        for u in record['waiting']:
                            edge = GraphEdge(u, locked_by, filename, record_id, snapshot)
                            graph.add_edge(edge)
        return graph
