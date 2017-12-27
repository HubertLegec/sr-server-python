
class Client:
    def __init__(self, sid):
        self.__sid = sid
        self.__login = None

    def get_login(self):
        return self.__login

    def set_login(self, login):
        self.__login = login

    def get_sid(self):
        return self.__sid
