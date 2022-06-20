from abc import ABCMeta, abstractmethod


class AbstractFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_tile(self, name, effect=None, doors=None, x=16, y=16,
                    entrance=None):
        pass
