from server.utils import ConfigLoader
import os


def test_config_reads_server_list():
    filename = os.path.dirname(__file__) + '/test_config.json'
    config = ConfigLoader(filename, 1)
    assert config.get_server_host() == '0.0.0.0'
    assert config.get_server_port() == 4201
    assert len(config.get_servers()) == 2
