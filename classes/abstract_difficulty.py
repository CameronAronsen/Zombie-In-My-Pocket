from abc import ABCMeta, abstractmethod


class AbstractDifficulty(metaclass=ABCMeta):
    @abstractmethod
    def set_difficulty(self):
        pass
