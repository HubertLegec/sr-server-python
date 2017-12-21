from . import File


class DirectoryController:
    def __init__(self):
        self.__files = []

    def get_files(self):
        return self.__files

    def get_file(self, name):
        filtered = [f for f in self.__files if f.get_name() == name]
        if len(filtered) == 0:
            raise RuntimeError("File with name " + name + "doesn't exist")
        return filtered[0]

    def create_file(self, name):
        name_exists = self.__check_if_name_exists(name)
        if name_exists:
            raise RuntimeError("File with name " + name + " already exists")
        file = File(name)
        self.__files.append(file)
        return file

    def delete_file(self, name):
        self.__files = [f for f in self.__files if f.get_name() != name]
        return None

    def __check_if_name_exists(self, name):
        filtered = [f for f in self.__files if f.get_name() == name]
        return len(filtered) > 0
