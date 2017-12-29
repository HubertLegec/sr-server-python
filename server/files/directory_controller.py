from . import File


class DirectoryController:
    def __init__(self, clients_controller):
        self.__files = []
        self.__clients_controller = clients_controller

    def get_files(self):
        return self.__files

    def get_file(self, name):
        filtered = [f for f in self.__files if f.get_name() == name]
        if len(filtered) == 0:
            raise FileNotFoundError("File with name " + name + " doesn't exist")
        return filtered[0]

    def create_file(self, name):
        name_exists = self.__check_if_name_exists(name)
        if name_exists:
            raise FileExistsError("File with name " + name + " already exists")
        file = File(name)
        self.__files.append(file)
        return file

    def delete_file(self, name):
        self.__files = [f for f in self.__files if f.get_name() != name]
        return None

    def add_opened_by(self, name, user):
        file = next(f for f in self.__files if f.get_name() == name)
        return file.add_opened_by(user)

    def remove_opened_by(self, name, user):
        file = next(f for f in self.__files if f.get_name() == name)
        file.remove_opened_by(user)

    def __check_if_name_exists(self, name):
        filtered = [f for f in self.__files if f.get_name() == name]
        return len(filtered) > 0
