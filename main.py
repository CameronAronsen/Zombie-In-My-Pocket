from directions import Direction as dir
import pandas as pd


class Game:
    def __init__(self, player, time=9, tiles=None, available_tiles=None):
        if available_tiles is None:
            available_tiles = []  # Will contain a list of all available tiles
        if tiles is None:
            tiles = {}  # Tiles dictionary will have the x and y co-ords as the key and the Tile object as the value
        self.player = player
        self.time = time
        self.available_tiles = available_tiles
        self.tiles = tiles

    def start_game(self):
        for tile in self.available_tiles:
            if tile.name == 'Patio':
                tile.set_exit(dir.NORTH)
                patio = tile
                self.tiles[(patio.x, patio.y)] = patio
                break

    def draw_card(self):
        pass

    def get_game(self):
        return print(f'The player has {self.player.get_health()} health and {self.player.get_attack()} attack the '
                     f'time is {self.time}')

    def load_tiles(self):  # Needs Error handling in this function
        excel_data = pd.read_excel('Tiles.xlsx')
        tiles = []
        for name in excel_data.iterrows():
            tiles.append(name[1].tolist())
        for tile in tiles:
            if tile[2] == "Outdoor":
                new_tile = OutdoorTile(tile[0], tile[1])
                self.available_tiles.append(new_tile)
            if tile[2] == "Indoor":
                new_tile = IndoorTile(tile[0], tile[1])
                self.available_tiles.append(new_tile)


class Player:
    def __init__(self, attack=1, health=6):
        self.attack = attack
        self.health = health

    def get_health(self):
        return self.health

    def get_attack(self):
        return self.attack

    def set_attack(self, attack):
        self.attack = attack

    def set_health(self, health):
        self.health = health


class DevCards:
    def __init__(self):
        pass


class Tile:
    def __init__(self, name, x=0, y=0, effect=None, entrance=None, ex=None):
        self.name = name
        self.x = x
        self.y = y
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
        return f'This tile is {self.name}, {self.entrance}, {self.exit}, {self.type},' \
               f' {self.x} {self.y} {self.effect} \n'


class OutdoorTile(Tile):
    def __init__(self, name, effect=None, x=0, y=0, entrance=None, ex=None):
        self.type = "Outdoor"
        super().__init__(name, x, y, effect, entrance, ex)

    def __repr__(self):
        return f'This tile is {self.name}, {self.entrance}, {self.exit},' \
               f' {self.type}, {self.x}, {self.y}, {self.effect} \n'


def main():
    player = Player()
    game = Game(player)
    game.load_tiles()
    game.get_game()
    game.start_game()


if __name__ == "__main__":
    main()
