from classes.directions import Direction as d
from classes.abstract_tile import Tile


class IndoorTile(Tile):
    """
    >>> from classes.tile import IndoorTile
    >>> from classes.directions import Direction as d
    >>> tile = IndoorTile("Family Room", x=0, y=0)
    >>> tile.get_name()
    'Family Room'
    >>> print(tile)
    Family Room, [], Indoor, 0, 0, None
    >>> tile.set_entrance(d.NORTH)
    >>> tile.get_entrance()
    <Direction.NORTH: (1,)>
    >>> tile.rotate_entrance()
    >>> tile.get_entrance()
    <Direction.EAST: (3,)>
    >>> tile.set_x(1)
    >>> tile.set_y(1)
    >>> tile.get_x()
    1
    >>> tile.get_y()
    1

    """
    def __init__(
        self, name, effect=None, doors=None, x=16, y=16, entrance=None
    ):
        if doors is None:
            doors = []
        self.type = "Indoor"
        super().__init__(name, x, y, effect, doors, entrance)

    def __repr__(self):
        return (
            f"{self.name}, {self.doors}, {self.type},"
            f" {self.x}, {self.y}, {self.effect}"
        )


class OutdoorTile(Tile):
    """
    >>> from classes.tile import OutdoorTile
    >>> from classes.directions import Direction as d
    >>> tile = OutdoorTile("Graveyard", x=0, y=0)
    >>> tile.get_name()
    'Graveyard'
    >>> print(tile)
    Graveyard, [], Outdoor, 0, 0, None
    >>> tile.set_entrance(d.SOUTH)
    >>> tile.get_entrance()
    <Direction.SOUTH: (2,)>
    >>> tile.rotate_entrance()
    >>> tile.rotate_entrance()
    >>> tile.get_entrance()
    <Direction.NORTH: (1,)>
    >>> tile.set_x(10)
    >>> tile.set_y(15)
    >>> tile.get_x()
    10
    >>> tile.get_y()
    15

    """
    def __init__(
        self, name, effect=None, doors=None, x=16, y=16, entrance=None
    ):
        if doors is None:
            doors = []
        self.type = "Outdoor"
        super().__init__(name, x, y, effect, doors, entrance)

    def __repr__(self):
        return (
            f"{self.name}, {self.doors}, {self.type},"
            f" {self.x}, {self.y}, {self.effect}"
        )
