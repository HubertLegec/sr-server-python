from server.utils import LogFactory
from . import Client


class ClientController:
    log = LogFactory.get_logger()

    def __init__(self, socketio):
        self.__clients = []
        self.__socketio = socketio

    def register_client(self, sid):
        self.__clients.append(Client(sid))

    def set_login_for_client(self, sid, login):
        client = next(c for c in self.__clients if c.get_sid() == sid)
        client.set_login(login)

    def remove_client(self, sid):
        self.__clients = [c for c in self.__clients if c.get_sid() != sid]

    def emit(self, clients, event_name, event_body=None):
        for client_name in clients:
            self.log.info('Emit to ' + client_name + ' event ' + event_name)
            client = self.get_client_by_name(client_name)
            self.__socketio.emit(event_name, event_body, room=client.get_login())

    def get_client_by_sid(self, sid):
        matching_clients = [c for c in self.__clients if c.get_sid() == sid]
        return matching_clients[0] if len(matching_clients) > 0 else None

    def get_client_by_name(self, name):
        matching_clients = [c for c in self.__clients if c.get_login() == name]
        return matching_clients[0] if len(matching_clients) > 0 else None

    def get_all_clients(self):
        return self.__clients
