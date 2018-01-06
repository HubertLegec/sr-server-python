from server.utils import Queue


def test_queue():
    queue = Queue()
    assert queue.size() == 0
    assert queue.pop() is None

    queue.put(1)
    assert queue.size() == 1
    queue.put(2)
    queue.put(3)
    assert queue.size() == 3
    queue.remove_by(lambda x: x == 2)
    assert queue.pop() == 1
    assert queue.pop() == 3
    assert queue.size() == 0
    assert queue.pop() is None