from multiprocessing import Lock


class Queue:
    def __init__(self):
        self.__lock = Lock()
        self.__queue = []

    def put(self, item):
        self.__lock.acquire()
        self.__queue.append(item)
        self.__lock.release()

    def pop(self):
        self.__lock.acquire()
        item = None if len(self.__queue) == 0 else self.__queue.pop(0)
        self.__lock.release()
        return item

    def size(self):
        return len(self.__queue)

    def remove_by(self, predicate):
        self.__lock.acquire()
        size_before = self.size()
        self.__queue = [i for i in self.__queue if not predicate(i)]
        size_after = self.size()
        self.__lock.release()
        return size_before != size_after
