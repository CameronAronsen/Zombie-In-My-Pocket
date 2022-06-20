from classes.abstract_factory import AbstractFactory
from classes.tile import *


class OutdoorFactory(AbstractFactory):
    def create_tile(self, name, effect=None, doors=None, x=16, y=16,
                    entrance=None):
        return OutdoorTile(name, effect, doors, x, y, entrance)
