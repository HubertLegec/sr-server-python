from . import Client


class ClientController:
    def __init__(self):
        self.__clients = []

    def register_client(self, login):
        self.__clients.append(Client(login))
