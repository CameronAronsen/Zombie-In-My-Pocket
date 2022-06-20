from classes.directions import Direction as d
from abc import ABCMeta


class Tile(metaclass=ABCMeta):
    def __init__(
        self, name, x=16, y=16, effect=None, doors=None, entrance=None
    ):
        self.name = name
        self.x = x
        self.y = y
        self.effect = effect
        self.doors = doors
        self.entrance = entrance

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_name(self):
        return self.name

    def change_door_position(self, idx, direction):
        self.doors[idx] = direction

    def get_door_position(self, idx):
        return self.doors[idx]
    
    def get_doors(self):
        return self.doors

    def get_entrance(self):
        return self.entrance

    def set_entrance(self, direction):
        self.entrance = direction

    def rotate_entrance(self):
        if self.entrance == d.NORTH:
            self.set_entrance(d.EAST)
            return
        elif self.entrance == d.SOUTH:
            self.set_entrance(d.WEST)
            return
        elif self.entrance == d.EAST:
            self.set_entrance(d.SOUTH)
            return
        else:
            self.set_entrance(d.NORTH)
            return

    # Will rotate the tile one position clockwise
    def rotate_tile(self):
        for door in self.doors:
            if door == d.NORTH:
                self.change_door_position(self.doors.index(door), d.EAST)
            if door == d.EAST:
                self.change_door_position(self.doors.index(door), d.SOUTH)
            if door == d.SOUTH:
                self.change_door_position(self.doors.index(door), d.WEST)
            if door == d.WEST:
                self.change_door_position(self.doors.index(door), d.NORTH)