from . import DeadlockDetector
from . import SnapshotDescription


def test_create_wait_for_graph():
    s1 = {
        'f1': {
            'r1': {
                'lockedBy': 'U4',
                'waiting': [
                    {'userId': 'U1', 'timestamp': '2017-01-03T14:50:02'},
                    {'userId': 'U2', 'timestamp': '2017-01-03T14:51:01'},
                    {'userId': 'U3', 'timestamp': '2017-01-03T14:52:12'}
                ]
            },
            'r2': {
                'lockedBy': 'U5',
                'waiting': [
                    {'userId': 'U4', 'timestamp': '2017-01-03T14:53:09'},
                    {'userId': 'U1', 'timestamp': '2017-01-03T14:55:03'}
                ]
            }
        }
    }
    s2 = {
        'f1': {
            'r1': {
                'lockedBy': 'U1',
                'waiting': [
                    {'userId': 'U5', 'timestamp': '2017-01-03T14:52:07'},
                    {'userId': 'U3', 'timestamp': '2017-01-03T14:53:01'}
                ]
            },
            'r2': {
                'lockedBy': 'U4',
                'waiting': [
                    {'userId': 'U1', 'timestamp': '2017-01-03T14:58:00'}
                ]
            }
        }
    }
    snapshots = [
        SnapshotDescription(s1, {'host': 'localhost', 'port': '4200'}),
        SnapshotDescription(s2, {'host': 'localhost', 'port': '4201'})
    ]

    wait_for_graph = DeadlockDetector.build_wait_for_graph(snapshots).get_graph()
    assert len(wait_for_graph.keys()) == 5
    assert len(wait_for_graph['U1'].keys()) == 2
    assert wait_for_graph['U1']['U4'][0].timestamp == '2017-01-03T14:50:02'
    assert wait_for_graph['U1']['U4'][1].timestamp == '2017-01-03T14:58:00'
    assert wait_for_graph['U1']['U5'][0].timestamp == '2017-01-03T14:55:03'
    assert len(wait_for_graph['U2'].keys()) == 1
    assert wait_for_graph['U2']['U4'][0].timestamp == '2017-01-03T14:51:01'
    assert len(wait_for_graph['U3'].keys()) == 2
    assert wait_for_graph['U3']['U4'][0].timestamp == '2017-01-03T14:52:12'
    assert wait_for_graph['U3']['U1'][0].timestamp == '2017-01-03T14:53:01'
    assert len(wait_for_graph['U4'].keys()) == 1
    assert wait_for_graph['U4']['U5'][0].timestamp == '2017-01-03T14:53:09'
    assert len(wait_for_graph['U5'].keys()) == 1
    assert wait_for_graph['U5']['U1'][0].timestamp == '2017-01-03T14:52:07'
