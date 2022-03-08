import random
from directions import Direction as d
import pandas as pd


class Game:
    def __init__(self, player, time=9, game_map=None, indoor_tiles=None, outdoor_tiles=None, current_tile=None):
        if indoor_tiles is None:
            indoor_tiles = []  # Will contain a list of all available indoor tiles
        if outdoor_tiles is None:
            outdoor_tiles = []  # Will contain a list of all available outdoor tiles
        if game_map is None:
            game_map = {}  # Tiles dictionary will have the x and y co-ords as the key and the Tile object as the value
        self.player = player
        self.time = time
        self.indoor_tiles = indoor_tiles
        self.outdoor_tiles = outdoor_tiles
        self.tiles = game_map
        self.current_tile = current_tile

    def start_game(self):
        for tile in self.indoor_tiles:
            if tile.name == 'Foyer':  # Game always starts in the Foyer
                self.current_tile = tile
                self.indoor_tiles.pop(self.indoor_tiles.index(tile))
                break

    def get_game(self):
        print(self.tiles)
        return print(f'The player has {self.player.get_health()} health and {self.player.get_attack()} attack the '
                     f'time is {self.time}, player is at {self.player.get_x(), self.player.get_y()} the current tile'
                     f' {self.current_tile} the player is at {self.get_current_tile()}')

    def load_tiles(self):  # Needs Error handling in this method
        excel_data = pd.read_excel('Tiles.xlsx')
        tiles = []
        for name in excel_data.iterrows():
            tiles.append(name[1].tolist())
        for tile in tiles:
            doors = self.resolve_doors(tile[3], tile[4], tile[5], tile[6])
            if tile[2] == "Outdoor":
                new_tile = OutdoorTile(tile[0], tile[1], doors)
                self.outdoor_tiles.append(new_tile)
            if tile[2] == "Indoor":
                new_tile = IndoorTile(tile[0], tile[1], doors)
                self.indoor_tiles.append(new_tile)

    def draw_tile(self, direction):
        if self.check_move_validity(direction):
            if self.current_tile.type == "Indoor":  # will need to be changed for the dining room
                tile = random.choice(self.indoor_tiles)  # Chooses a random indoor tile
            elif self.current_tile.type == "Outdoor":  # will need to be changed for the patio
                tile = random.choice(self.outdoor_tiles)  # Chooses a random outdoor tile
            if direction == d.NORTH:
                tile.set_y(tile.y - 1)
            if direction == d.SOUTH:
                tile.set_y(tile.y + 1)
            if direction == d.NORTH:
                tile.set_x(tile.x - 1)
            if direction == d.NORTH:
                tile.set_x(tile.x + 1)
            self.current_tile = tile

    def place_tile(self):
        tile = self.current_tile
        self.tiles[(tile.x, tile.y)] = tile
        if tile.type == "Outdoor":
            self.outdoor_tiles.pop(self.outdoor_tiles.index(tile))
        elif tile.type == "indoor":
            self.indoor_tiles.pop(self.indoor_tiles.index(tile))

    def get_current_tile(self):  # returns the current tile that the player is at
        return self.tiles[self.player.get_x(), self.player.get_y()]

    def move_player(self, direction):
        if direction == d.NORTH:
            if self.check_move_validity(d.NORTH):
                self.player.set_y(self.player.get_y() - 1)
        if direction == d.SOUTH:
            if self.check_move_validity(d.SOUTH):
                self.player.set_y(self.player.get_y() + 1)
        if direction == d.EAST:
            if self.check_move_validity(d.EAST):
                self.player.set_y(self.player.get_x() - 1)
        if direction == d.WEST:
            if self.check_move_validity(d.WEST):
                self.player.set_y(self.player.get_x() + 1)
        else:
            print("Invalid Input")

    def check_move_validity(self, direction):
        if direction == d.NORTH:
            if d.SOUTH in self.current_tile.doors and d.NORTH in self.current_tile.doors:
                return True
        if direction == d.SOUTH:
            if d.NORTH in self.current_tile.doors and d.SOUTH in self.current_tile.doors:
                return True
        if direction == d.EAST:
            if d.WEST in self.current_tile.doors and d.EAST in self.current_tile.doors:
                return True
        if direction == d.WEST:
            if d.EAST in self.current_tile.doors and d.WEST in self.current_tile.doors:
                return True
        return False

    def rotate(self):
        tile = self.current_tile
        tile.rotate_tile()

    @staticmethod
    def resolve_doors(n, e, s, w):
        doors = []
        if n == 1:
            doors.append(d.NORTH)
        if e == 1:
            doors.append(d.EAST)
        if s == 1:
            doors.append(d.SOUTH)
        if w == 1:
            doors.append(d.WEST)
        return doors


class Player:
    def __init__(self, attack=1, health=6, x=16, y=16):
        self.attack = attack
        self.health = health
        self.x = x  # x Will represent the players position horizontally starts at 16
        self.y = y  # y will represent the players position vertically starts at 16

    def get_health(self):
        return self.health

    def get_attack(self):
        return self.attack

    def set_attack(self, attack):
        self.attack = attack

    def set_health(self, health):
        self.health = health

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class DevCards:
    def __init__(self):
        pass


class Tile:
    def __init__(self, name, x=16, y=16, effect=None, doors=None):
        if doors is None:
            doors = []
        self.name = name
        self.x = x  # x will represent the tiles position horizontally
        self.y = y  # y will represent the tiles position vertically
        self.effect = effect
        self.doors = doors

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def change_door_position(self, idx, direction):
        self.doors[idx] = direction

    def rotate_tile(self):  # Will rotate the tile 1 position clockwise
        for door in self.doors:
            if door == d.NORTH:
                self.change_door_position(self.doors.index(door), d.EAST)
            if door == d.EAST:
                self.change_door_position(self.doors.index(door), d.SOUTH)
            if door == d.SOUTH:
                self.change_door_position(self.doors.index(door), d.WEST)
            if door == d.WEST:
                self.change_door_position(self.doors.index(door), d.NORTH)


class IndoorTile(Tile):
    def __init__(self, name, effect=None, doors=None, x=16, y=16):
        if doors is None:
            doors = []
        self.type = "Indoor"
        super().__init__(name, x, y, effect, doors)

    def __repr__(self):
        return f'{self.name}, {self.doors}, {self.type},' \
               f' {self.x}, {self.y}, {self.effect} \n'


class OutdoorTile(Tile):
    def __init__(self, name, effect=None, doors=None, x=16, y=16):
        if doors is None:
            doors = []
        self.type = "Outdoor"
        super().__init__(name, x, y, effect, doors)

    def __repr__(self):
        return f'{self.name}, {self.doors}, {self.type},' \
               f' {self.x}, {self.y}, {self.effect} \n'


def main():
    player = Player()
    game = Game(player)
    game.load_tiles()
    game.start_game()
    game.rotate()
    game.rotate()
    game.rotate()
    game.place_tile()
    game.draw_tile(d.NORTH)
    game.draw_tile(d.SOUTH)
    game.get_game()


if __name__ == "__main__":
    main()
