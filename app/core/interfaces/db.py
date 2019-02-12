import abc


class DbInterface(abc.ABC):
    @abc.abstractmethod
    def save(self, objects):
        pass

    @abc.abstractmethod
    def get(self):
        pass

    @abc.abstractmethod
    def get_all(self):
        pass
