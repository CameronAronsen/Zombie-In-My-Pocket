import random
from directions import Direction as d
import pandas as pd


class Game:
    def __init__(self, player, time=9, tiles=None, indoor_tiles=None, outdoor_tiles=None):
        if indoor_tiles is None:
            indoor_tiles = []  # Will contain a list of all available indoor tiles
        if outdoor_tiles is None:
            outdoor_tiles = []  # Will contain a list of all available outdoor tiles
        if tiles is None:
            tiles = {}  # Tiles dictionary will have the x and y co-ords as the key and the Tile object as the value
        self.player = player
        self.time = time
        self.indoor_tiles = indoor_tiles
        self.outdoor_tiles = outdoor_tiles
        self.tiles = tiles

    def start_game(self):
        for tile in self.indoor_tiles:
            if tile.name == 'Foyer':  # Game always starts in the Foyer at 0,0
                tile.set_exit(d.NORTH)
                self.place_tile(tile)
                break
        print(self.indoor_tiles)
        print(self.outdoor_tiles)

    def draw_card(self):
        pass

    def get_game(self):
        print(self.tiles)
        return print(f'The player has {self.player.get_health()} health and {self.player.get_attack()} attack the '
                     f'time is {self.time}, the player is at {self.player.get_x(), self.player.get_y()} or the'
                     f' {self.get_current_tile().name}')

    def load_tiles(self):  # Needs Error handling in this method
        excel_data = pd.read_excel('Tiles.xlsx')
        tiles = []
        for name in excel_data.iterrows():
            tiles.append(name[1].tolist())
        for tile in tiles:
            if tile[2] == "Outdoor":
                new_tile = OutdoorTile(tile[0], tile[1])
                self.outdoor_tiles.append(new_tile)
            if tile[2] == "Indoor":
                new_tile = IndoorTile(tile[0], tile[1])
                self.indoor_tiles.append(new_tile)

    def draw_indoor_tile(self, x, y, entrance, ex):
        tile = random.choice(self.indoor_tiles)  # Chooses a random outdoor tile and places it
        tile.set_entrance(entrance)
        tile.set_exit(ex)
        tile.set_x(x)
        tile.set_y(y)
        self.place_tile(tile)

    def draw_outdoor_tile(self, x, y, entrance):
        tile = random.choice(self.outdoor_tiles)  # Chooses a random outdoor tile and places it
        tile.set_entrance(entrance)
        tile.set_x(x)
        tile.set_y(y)
        self.place_tile(tile)

    def place_tile(self, tile):
        self.tiles[(tile.x, tile.y)] = tile
        if tile.type == "Outdoor":
            self.outdoor_tiles.pop(self.outdoor_tiles.index(tile))
        elif tile.type == "indoor":
            self.indoor_tiles.pop(self.indoor_tiles.index(tile))

    def get_current_tile(self):  # returns the current tile that the player is at
        return self.tiles[self.player.get_x(), self.player.get_y()]

    def move_player(self, direction):
        if direction == d.NORTH:
            self.player.set_y(self.player.get_y() + 1)
        if direction == d.SOUTH:
            self.player.set_y(self.player.get_y() - 1)
        if direction == d.EAST:
            self.player.set_y(self.player.get_x() + 1)
        if direction == d.WEST:
            self.player.set_y(self.player.get_x() - 1)


class Player:
    def __init__(self, attack=1, health=6, x=0, y=0):
        self.attack = attack
        self.health = health
        self.x = x  # x Will represent the players position horizontally
        self.y = y  # y will represent the players position vertically

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
    def __init__(self, name, x=0, y=0, effect=None, entrance=None, ex=None):
        self.name = name
        self.x = x  # x will represent the tiles position horizontally
        self.y = y  # y will represent the tiles position vertically
        self.effect = effect
        self.entrance = entrance
        self.exit = ex

    def set_exit(self, direction):
        self.exit = direction

    def set_entrance(self, direction):
        self.entrance = direction

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y


class IndoorTile(Tile):
    def __init__(self, name, effect=None, x=0, y=0, entrance=None, ex=None):
        self.type = "Indoor"
        super().__init__(name, x, y, effect, entrance, ex)

    def __repr__(self):
        return f'{self.name}, {self.entrance}, {self.exit}, {self.type},' \
               f' {self.x}, {self.y}, {self.effect} \n'


class OutdoorTile(Tile):
    def __init__(self, name, effect=None, x=0, y=0, entrance=None, ex=None):
        self.type = "Outdoor"
        super().__init__(name, x, y, effect, entrance, ex)

    def __repr__(self):
        return f' {self.name}, {self.entrance}, {self.exit},' \
               f' {self.type}, {self.x}, {self.y}, {self.effect} \n'


def main():
    player = Player()
    game = Game(player)
    game.load_tiles()
    game.start_game()
    game.draw_indoor_tile(0, 1, d.NORTH, d.EAST)
    game.move_player(d.NORTH)
    game.get_game()


if __name__ == "__main__":
    main()
