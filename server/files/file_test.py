import pytest
from . import File


def test_file_creates_records():
    file = File('file 1')
    content = 'record content'
    id = file.create_record(content).get_id()

    assert file.get_record(id).get_content() == content


def test_error_when_record_not_found():
    file = File('file 1')

    with pytest.raises(RuntimeError):
        file.get_record(1)
