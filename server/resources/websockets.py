from flask_socketio import Namespace, join_room, leave_room, close_room
from flask import request

from server.utils import LogFactory


class WebsocketNamespace(Namespace):
    log = LogFactory.get_logger()

    def __init__(self, clients_controller, directory_controller, file_controller):
        super(WebsocketNamespace, self).__init__('/')
        self.clients_controller = clients_controller
        self.dir_controller = directory_controller
        self.file_controller = file_controller

    def on_connect(self):
        sid = request.sid
        self.clients_controller.register_client(sid)
        self.log.info('New user #%s connected', sid)

    def on_disconnect(self):
        sid = request.sid
        client = self.clients_controller.get_client_by_sid(sid)
        if client:
            self.dir_controller.disconnect_user(client.get_login())
            self.clients_controller.remove_client(sid)
            close_room(client.get_login())
            self.log.info('Room ' + client.get_login() + ' removed')
        self.log.info('User #%s disconnected', sid)

    def on_authorize(self, json):
        login = json['userId']
        sid = request.sid
        join_room(login)
        self.clients_controller.set_login_for_client(sid, login)
        self.log.info('User #%s authorized with login: %s', sid, login)

    def on_file_state_change(self, json):
        event_type = json['eventType']
        filename = json['file']
        username = json['userId']
        self.log.info("Event: %s for file: %s send by: %s", event_type, filename, username)
        if event_type == "OPEN_FILE":
            self.dir_controller.add_opened_by(filename, username)
        elif event_type == "CLOSE_FILE":
            self.dir_controller.remove_opened_by(filename, username)
        else:
            raise ValueError("Invalid eventType")

    def on_record_state_change(self, json):
        event_type = json['eventType']
        filename = json['file']
        record_id = json['record']
        username = json['userId']
        if event_type == "LOCK_RECORD":
            self.file_controller.lock_record(filename, record_id, username)
        elif event_type == "UNLOCK_RECORD":
            self.file_controller.unlock_record(filename, record_id, username)
        self.log.info("Event: %s for record #%d in file: %s by user: %s", event_type, record_id, filename, username)
