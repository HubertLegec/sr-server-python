from dateutil import parser


class WaitForGraph:
    def __init__(self):
        self.__graph = {}

    def add_edge(self, e):
        if e.waiting_user in self.__graph:
            if e.locking_user in self.__graph[e.waiting_user]:
                self.__graph[e.waiting_user][e.locking_user].append(e)
            else:
                self.__graph[e.waiting_user][e.locking_user] = [e]
        else:
            self.__graph[e.waiting_user] = {}
            self.__graph[e.waiting_user][e.locking_user] = [e]

    def remove_edge(self, e):
        w_user = e.waiting_user
        l_user = e.locking_user
        self.__graph[w_user][l_user].remove(e)
        if len(self.__graph[w_user][l_user]) == 0:
            self.__graph[w_user].pop(l_user)
            if len(self.__graph[w_user].keys()) == 0:
                self.__graph.pop(w_user)

    @classmethod
    def get_youngest_edge(cls, edges):
        return max(edges, key=lambda e: parser.parse(e.timestamp))

    def find_cycle(self):
        if len(self.__graph.keys()) < 2:
            return None
        visited = set()
        path = [object()]
        path_set = set(path)
        stack = [iter(self.__graph)]
        while stack:
            for v in stack[-1]:
                if v in path_set:
                    return self.map_users_cycle_to_edges(path[1:])
                elif v not in visited:
                    visited.add(v)
                    path.append(v)
                    path_set.add(v)
                    stack.append(iter(self.__graph.get(v, ())))
                    break
            else:
                path_set.remove(path.pop())
                stack.pop()
        return None

    def get_graph(self):
        return self.__graph

    def map_users_cycle_to_edges(self, cycle):
        result = []
        cycle_size = len(cycle)
        for idx in range(cycle_size):
            u1 = cycle[idx]
            u2 = cycle[(idx + 1) % cycle_size]
            edges = self.__graph[u1][u2]
            e = self.get_youngest_edge(edges)
            result.append(e)
        return result
