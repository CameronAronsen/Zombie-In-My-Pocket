import unittest
from classes.tile import *
from classes.abstract_tile import Tile
from classes.outdoor_factory import OutdoorFactory
from classes.indoor_factory import IndoorFactory


class TestIndoorTiles(unittest.TestCase):
    def setUp(self):
        self.indoor_factory = IndoorFactory()
        self.indoor_tile = self.indoor_factory.create_tile(
            name="Kitchen", doors=[d.NORTH, d.EAST, d.SOUTH], entrance=d.NORTH
            )

    def test_tile_has_x(self):
        self.indoor_tile.set_x(5)
        self.assertEqual(self.indoor_tile.get_x(), 5)

    def test_tile_has_y(self):
        self.indoor_tile.set_y(5)
        self.assertEqual(self.indoor_tile.get_y(), 5)

    def test_indoor_tile_has_name(self):
        self.assertEqual(self.indoor_tile.get_name(), "Kitchen")

    def test_get_door_position(self):
        self.indoor_tile.change_door_position(0, d.EAST)
        self.indoor_tile.rotate_tile()
        self.indoor_tile.rotate_tile()
        self.indoor_tile.rotate_tile()
        self.indoor_tile.rotate_tile()
        self.indoor_tile.rotate_tile()
        self.assertEqual(self.indoor_tile.get_door_position(0), d.WEST)

    def test_indoor_tile_has_entrance(self):
        self.indoor_tile.set_entrance(d.NORTH)
        self.indoor_tile.rotate_entrance()
        self.indoor_tile.rotate_entrance()
        self.indoor_tile.rotate_entrance()
        self.indoor_tile.rotate_entrance()
        self.indoor_tile.rotate_entrance()
        self.assertEqual(self.indoor_tile.get_entrance(), d.EAST)

    def test_tile_without_doors(self):
        self.indoor_tile = IndoorTile(name="Kitchen", entrance=d.NORTH)
        self.assertEqual(self.indoor_tile.get_doors(), [])

    def test_tile_description(self):
        self.assertEqual(
            repr(self.indoor_tile),
            f"Kitchen, [<Direction.NORTH: (1,)>, <Direction.EAST: (3,)>, "
            f"<Direction.SOUTH: (2,)>], Indoor, 16, 16, None",
        )


class TestOutdoorTiles(unittest.TestCase):
    def setUp(self):
        self.outdoor_factory = OutdoorFactory()
        self.outdoor_tile = self.outdoor_factory.create_tile(
            name="Yard", doors=[d.NORTH, d.EAST, d.SOUTH], entrance=d.NORTH
            )

    def test_tile_has_x(self):
        self.outdoor_tile.set_x(5)
        self.assertEqual(self.outdoor_tile.get_x(), 5)

    def test_tile_has_y(self):
        self.outdoor_tile.set_y(5)
        self.assertEqual(self.outdoor_tile.get_y(), 5)

    def test_outdoor_tile_has_name(self):
        self.assertEqual(self.outdoor_tile.get_name(), "Yard")

    def test_get_door_position(self):
        self.outdoor_tile.change_door_position(0, d.EAST)
        self.outdoor_tile.rotate_tile()
        self.assertEqual(self.outdoor_tile.get_door_position(0), d.WEST)

    def test_indoor_tile_has_entrance(self):
        self.outdoor_tile.set_entrance(d.NORTH)
        self.outdoor_tile.rotate_entrance()
        self.assertEqual(self.outdoor_tile.get_entrance(), d.EAST)

    def test_tile_without_doors(self):
        self.outdoor_tile = OutdoorTile(name="Yard", entrance=d.NORTH)
        self.assertEqual(self.outdoor_tile.get_doors(), [])

    def test_tile_description(self):
        self.assertEqual(
            repr(self.outdoor_tile),
            f"Yard, [<Direction.NORTH: (1,)>, <Direction.EAST: (3,)>, "
            f"<Direction.SOUTH: (2,)>], "
            f"Outdoor, 16, 16, None",
        )


if __name__ == "__main__":
    unittest.main()
