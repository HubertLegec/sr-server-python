from datetime import datetime


class WaitingClient:
    def __init__(self, user_id):
        self.__user_id = user_id
        self.__timestamp = datetime.utcnow()

    def get_user(self):
        return self.__user_id

    def get_timestamp(self):
        return self.__timestamp

    def update_timestamp(self):
        self.__timestamp = datetime.utcnow()

    def to_dictionary(self):
        return {
            'userId': self.__user_id,
            'timestamp': self.__timestamp
        }
