import pytest
from . import File


def test_file_creates_records():
    file = File('file 1')
    content = 'record content'
    id = file.create_record(content).get_id()

    assert file.get_record(id).get_content() == content


def test_error_when_record_not_found():
    file = File('file 1')

    with pytest.raises(FileNotFoundError):
        file.get_record(1)


def test_find_empty_record_idx():
    ids = [0, 1, 2, 4, 6]
    assert File.smallest_not_in_list(ids) == 3

    ids2 = []
    assert File.smallest_not_in_list(ids2) == 0

    ids3 = [0, 1, 2]
    assert File.smallest_not_in_list(ids3) == 3