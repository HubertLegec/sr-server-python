import schedule
import time


class DeadlockController:
    def __init__(self):
        None

    def run(self):
        None

    @staticmethod
    def detect_deadlocks(self):
        return None

    @staticmethod
    def build_wait_for_graph(snapshots):
        graph = {}
        for snapshot in snapshots:
            files = snapshot.keys()
            for file_name in files:
                file = snapshot[file_name]
                records = file.keys()
                for record_id in records:
                    record = file[record_id]
                    locked_by = record['lockedBy']
                    if locked_by:
                        waiting = [u['userId'] for u in record['waiting']]
                        for u in waiting:
                            DeadlockController.add_to_graph(graph, u, locked_by)
        return graph

    @staticmethod
    def add_to_graph(graph, v1, v2):
        if v1 in graph:
            graph[v1].append(v2)
        else:
            graph[v1] = [v2]

    @staticmethod
    def find_cycle(graph):
        if len(graph.keys()) < 2:
            return False
        visited = set()
        path = [object()]
        path_set = set(path)
        stack = [iter(graph)]
        while stack:
            for v in stack[-1]:
                if v in path_set:
                    return True, path[1:]
                elif v not in visited:
                    visited.add(v)
                    path.append(v)
                    path_set.add(v)
                    stack.append(iter(graph.get(v, ())))
                    break
            else:
                path_set.remove(path.pop())
                stack.pop()
        return False
