from . import DeadlockController


def test_create_wait_for_graph():
    snapshots = [{
        'f1': {
            'r1': {
                'lockedBy': 'U4',
                'waiting': [{'userId': 'U1'}, {'userId': 'U2'}, {'userId': 'U3'}]
            },
            'r2': {
                'lockedBy': 'U5',
                'waiting': [{'userId': 'U4'}, {'userId': 'U1'}]
            }
        }
    }, {
        'f1': {
            'r1': {
                'lockedBy': 'U1',
                'waiting': [{'userId': 'U5'}, {'userId': 'U3'}]
            }
        }
    }]

    wait_for_graph = DeadlockController.build_wait_for_graph(snapshots)
    assert len(wait_for_graph.keys()) == 5
    assert wait_for_graph['U1'] == ['U4', 'U5']
    assert wait_for_graph['U2'] == ['U4']
    assert wait_for_graph['U3'] == ['U4', 'U1']
    assert wait_for_graph['U4'] == ['U5']
    assert wait_for_graph['U5'] == ['U1']


def test_find_simple_cycle():
    graph = {
        '1': ['2'], '2': ['3'], '3': ['1']
    }
    path_exists, path = DeadlockController.find_cycle(graph)
    assert path_exists
    assert path == ['1', '2', '3']

    graph2 = {
        '1': ['2', '3'], '2': ['3'], '3': []
    }
    assert not DeadlockController.find_cycle(graph2)


def test_find_cycle():
    graph = {
        'U1': ['U4', 'U5'],
        'U2': ['U4'],
        'U3': ['U4', 'U1'],
        'U4': ['U5'],
        'U5': ['U1']
    }
    path_exists, path = DeadlockController.find_cycle(graph)
    assert path_exists
    assert path == ['U1', 'U4', 'U5']
