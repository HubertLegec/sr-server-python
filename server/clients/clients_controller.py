from . import Client


class ClientController:
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
            client = self.get_client_by_name(client_name)
            self.__socketio.emit(event_name, event_body, room=client.get_login())

    def get_client_by_name(self, name):
        return next(c for c in self.__clients if c.get_login() == name)

    def get_all_clients(self):
        return self.__clients
