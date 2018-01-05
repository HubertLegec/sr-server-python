import json

from . import LogFactory


class ConfigLoader:
    log = LogFactory.get_logger()

    def __init__(self, path, curr_server_id):
        self.config = self.__load_config(path)
        self.server_id = curr_server_id

    def __load_config(self, path):
        """Loads loads configuration from file"""
        self.log.info('Load config from path: ' + path)
        with open(path) as file:
            return json.load(file)

    def get_servers(self):
        servers = self.__get_all_servers()
        return servers[:self.server_id] + servers[(self.server_id + 1):]

    def get_server_host(self):
        servers = self.__get_all_servers()
        return servers[self.server_id]['host']

    def get_server_port(self):
        servers = self.__get_all_servers()
        return servers[self.server_id]['port']

    def __get_all_servers(self):
        return self.config['servers']
