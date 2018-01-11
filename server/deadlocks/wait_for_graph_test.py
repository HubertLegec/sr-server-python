from server.deadlocks import WaitForGraph
from server.deadlocks import GraphEdge
from server.deadlocks import SnapshotDescription


def test_find_simple_cycle():
    snapshot_descr = SnapshotDescription({}, {'host': 'localhost', 'port': '4200'})
    user1 = {'userId': '1', 'timestamp': '2017-01-03T14:55:03'}
    user2 = {'userId': '2', 'timestamp': '2017-01-03T14:56:03'}
    user3 = {'userId': '3', 'timestamp': '2017-01-03T14:57:03'}
    e1 = GraphEdge(user1, user2['userId'], 'f1', 1, snapshot_descr)
    e2 = GraphEdge(user2, user3['userId'], 'f1', 2, snapshot_descr)
    e3 = GraphEdge(user3, user1['userId'], 'f1', 3, snapshot_descr)
    graph = WaitForGraph()
    graph.add_edge(e1)
    graph.add_edge(e2)
    graph.add_edge(e3)
    cycle = graph.find_cycle()
    assert len(cycle) == 3
    assert cycle == [e1, e2, e3]

    last_edge = WaitForGraph.get_youngest_edge(cycle)
    graph.remove_edge(last_edge)
    assert graph.find_cycle() is None

    graph2 = WaitForGraph()
    graph2.add_edge(GraphEdge(user1, user2['userId'], 'f1', 1, snapshot_descr))
    graph2.add_edge(GraphEdge(user1, user3['userId'], 'f1', 2, snapshot_descr))
    graph2.add_edge(GraphEdge(user2, user3['userId'], 'f1', 3, snapshot_descr))

    assert graph2.find_cycle() is None


def test_find_cycle():
    snapshot_descr = SnapshotDescription({}, {'host': 'localhost', 'port': '4200'})
    user1 = {'userId': '1', 'timestamp': '2017-01-03T14:55:03'}
    user1_1 = {'userId': '1', 'timestamp': '2017-01-03T14:51:03'}
    user2 = {'userId': '2', 'timestamp': '2017-01-03T14:56:03'}
    user3 = {'userId': '3', 'timestamp': '2017-01-03T14:52:03'}
    user4 = {'userId': '4', 'timestamp': '2017-01-03T14:56:13'}
    user5 = {'userId': '5', 'timestamp': '2017-01-03T14:54:03'}

    e14 = GraphEdge(user1, user4['userId'], 'f1', 1, snapshot_descr)
    e15 = GraphEdge(user1, user5['userId'], 'f1', 2, snapshot_descr)
    e14_1 = GraphEdge(user1_1, user4['userId'], 'f2', 2, snapshot_descr)
    e24 = GraphEdge(user2, user4['userId'], 'f1', 1, snapshot_descr)
    e34 = GraphEdge(user3, user4['userId'], 'f1', 1, snapshot_descr)
    e31 = GraphEdge(user3, user1['userId'], 'f2', 1, snapshot_descr)
    e45 = GraphEdge(user4, user5['userId'], 'f1', 2, snapshot_descr)
    e51 = GraphEdge(user5, user1['userId'], 'f2', 1, snapshot_descr)
    graph = WaitForGraph()
    graph.add_edge(e14)
    graph.add_edge(e15)
    graph.add_edge(e14_1)
    graph.add_edge(e24)
    graph.add_edge(e34)
    graph.add_edge(e31)
    graph.add_edge(e45)
    graph.add_edge(e51)

    cycle = graph.find_cycle()
    assert cycle == [e14, e45, e51]
    youngest_edge = WaitForGraph.get_youngest_edge(cycle)
    graph.remove_edge(youngest_edge)

    cycle2 = graph.find_cycle()
    assert cycle2 == [e15, e51]
    youngest_edge2 = WaitForGraph.get_youngest_edge(cycle2)
    graph.remove_edge(youngest_edge2)

    cycle3 = graph.find_cycle()
    assert cycle3 is None
