import pytest
from . import Record


def test_lock_by_single_user():
    record = Record(1)
    assert record.get_locked_by() is None
    assert record.lock('user 1')
    assert record.get_locked_by() == 'user 1'
    assert record.get_waiting_users() == []
    assert record.unlock('user 1') is None
    assert record.get_locked_by() is None
    assert record.get_waiting_users() == []
    with pytest.raises(PermissionError):
        record.unlock('user 1')


def test_lock_by_two_users():
    record = Record(1)
    assert record.get_locked_by() is None
    assert record.get_waiting_users() == []
    assert record.lock('user 1')
    assert record.get_locked_by() == 'user 1'
    assert record.lock('user 2') is False
    assert record.get_locked_by() == 'user 1'
    assert len(record.get_waiting_users()) == 1
    assert record.unlock('user 1') == 'user 2'
    assert record.get_locked_by() == 'user 2'
    assert record.get_waiting_users() == []
    assert record.unlock('user 2') is None
