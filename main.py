import random
from directions import Direction as d
import pandas as pd
import cmd


class Game:
    def __init__(self, player, time=9, game_map=None, indoor_tiles=None, outdoor_tiles=None, chosen_tile=None,
                 state="Starting", current_move_direction=None):
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
        self.chosen_tile = chosen_tile
        self.state = state
        self.current_move_direction = current_move_direction

    def start_game(self):
        self.load_tiles()
        for tile in self.indoor_tiles:
            if tile.name == 'Foyer':  # Game always starts in the Foyer at 16,16
                self.chosen_tile = tile
                self.state = "Rotating"
                self.indoor_tiles.pop(self.indoor_tiles.index(tile))
                break

    def get_game(self):
        print(self.tiles)
        return print(f'the player is at {self.player.get_x(), self.player.get_y()}'
                     f' the chosen tile is {self.chosen_tile.name}, {self.chosen_tile.doors}'
                     f' the state is {self.state} ENTRANCE {self.chosen_tile.entrance}')

    def load_tiles(self):  # Needs Error handling in this method
        excel_data = pd.read_excel('Tiles.xlsx')
        tiles = []
        for name in excel_data.iterrows():
            tiles.append(name[1].tolist())
        for tile in tiles:
            doors = self.resolve_doors(tile[3], tile[4], tile[5], tile[6])
            if tile[2] == "Outdoor":
                new_tile = OutdoorTile(tile[0], tile[1], doors)
                if tile[0] == "Patio":
                    new_tile.set_entrance(d.NORTH)
                self.outdoor_tiles.append(new_tile)
            if tile[2] == "Indoor":
                new_tile = IndoorTile(tile[0], tile[1], doors)
                if tile[0] == "Dining Room":
                    new_tile.set_entrance(d.NORTH)
                self.indoor_tiles.append(new_tile)

    def draw_tile(self, x, y):
        if self.get_current_tile().type == "Indoor":
            tile = random.choice(self.indoor_tiles)  # Chooses a random indoor tile and places it
            tile.set_x(x)
            tile.set_y(y)
            self.chosen_tile = tile
            self.indoor_tiles.pop(self.indoor_tiles.index(tile))
        elif self.get_current_tile().type == "Outdoor":
            tile = random.choice(self.indoor_tiles)
            tile.set_x(x)
            tile.set_y(y)
            self.chosen_tile = tile
            self.outdoor_tiles.pop(self.outdoor_tiles.index(tile))

    def move_player(self, x, y):
        self.player.set_y(y)
        self.player.set_x(x)
        self.state = "Moving"  # State should be drawing card

    def select_move(self, direction):
        x, y = self.get_destination_coords(direction)
        if self.check_for_door(direction):  # If there's a door where the player tried to move
            if self.check_for_room(x, y) is False:
                self.draw_tile(x, y)
                self.current_move_direction = direction
                self.state = "Rotating"
            if self.check_for_room(x, y):
                self.current_move_direction = direction
                self.move_player(x, y)

    def get_destination_coords(self, direction):  # Gets the x and y value of the proposed move
        if direction == d.NORTH:
            return self.player.get_x(), self.player.get_y() - 1
        if direction == d.SOUTH:
            return self.player.get_x(), self.player.get_y() + 1
        if direction == d.EAST:
            return self.player.get_x() + 1, self.player.get_y()
        if direction == d.WEST:
            return self.player.get_x() - 1, self.player.get_y()

    def check_for_door(self, direction):  # Takes a direction and checks if the current room has a door there
        if direction in self.get_current_tile().doors:
            return True
        else:
            return False

    def check_for_room(self, x, y):  # Takes a move direction and checks if there is a room there
        if (x, y) not in self.tiles:
            return False
        else:
            self.chosen_tile = self.tiles[(x, y)]
            return True

    def check_doors_align(self, direction):
        if self.chosen_tile.name == "Foyer":
            return True
        if direction == d.NORTH:
            if d.SOUTH not in self.chosen_tile.doors:
                return False
        if direction == d.SOUTH:
            if d.NORTH not in self.chosen_tile.doors:
                return False
        if direction == d.WEST:
            if d.EAST not in self.chosen_tile.doors:
                return False
        elif direction == d.EAST:
            if d.WEST not in self.chosen_tile.doors:
                return False
        return True

    def place_tile(self, x, y):
        tile = self.chosen_tile
        self.tiles[(x, y)] = tile
        self.state = "Moving"
        if tile.type == "Outdoor":
            self.outdoor_tiles.pop(self.outdoor_tiles.index(tile))
        elif tile.type == "indoor":
            self.indoor_tiles.pop(self.indoor_tiles.index(tile))

    def get_current_tile(self):  # returns the current tile that the player is at
        return self.tiles[self.player.get_x(), self.player.get_y()]

    def rotate(self):
        tile = self.chosen_tile
        tile.rotate_tile()

    def draw_dev_card(self):
        pass

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
    def __init__(self, name, x=16, y=16, effect=None, doors=None, entrance=None):
        if doors is None:
            doors = []
        self.name = name
        self.x = x  # x will represent the tiles position horizontally
        self.y = y  # y will represent the tiles position vertically
        self.effect = effect
        self.doors = doors
        self.entrance = entrance

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def change_door_position(self, idx, direction):
        self.doors[idx] = direction

    def set_entrance(self, direction):
        self.entrance = direction

    def rotate_entrance(self):
        if self.entrance == d.NORTH:
            self.set_entrance(d.EAST)
        if self.entrance == d.SOUTH:
            self.set_entrance(d.WEST)
        if self.entrance == d.EAST:
            self.set_entrance(d.SOUTH)
        if self.entrance == d.WEST:
            self.set_entrance(d.NORTH)

    def rotate_tile(self):  # Will rotate the tile 1 position clockwise
        if self.name == "Dining Room" or self.name == "Patio":
            self.rotate_entrance()
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
    def __init__(self, name, effect=None, doors=None, x=16, y=16, entrance=None):
        if doors is None:
            doors = []
        self.type = "Indoor"
        super().__init__(name, x, y, effect, doors, entrance)

    def __repr__(self):
        return f'{self.name}, {self.doors}, {self.type},' \
               f' {self.x}, {self.y}, {self.effect} \n'


class OutdoorTile(Tile):
    def __init__(self, name, effect=None, doors=None, x=16, y=16, entrance=None):
        if doors is None:
            doors = []
        self.type = "Outdoor"
        super().__init__(name, x, y, effect, doors, entrance)

    def __repr__(self):
        return f'{self.name}, {self.doors}, {self.type},' \
               f' {self.x}, {self.y}, {self.effect} \n'


class Commands(cmd.Cmd):
    player = Player()
    game = Game(player)

    def do_start(self, line):
        if self.game.state == "Starting":
            self.game.start_game()
            self.game.get_game()
        else:
            print("Game has already Started")

    def do_rotate(self, line):
        if self.game.state == "Rotating":
            self.game.rotate()
            self.game.get_game()

    def do_place(self, line):
        if self.game.state == "Rotating":
            if self.game.chosen_tile.name == "Foyer":
                self.game.place_tile(16, 16)
                self.game.get_game()
            else:
                if self.game.check_doors_align(self.game.current_move_direction):
                    self.game.place_tile(self.game.chosen_tile.x, self.game.chosen_tile.y)
                    self.game.move_player(self.game.chosen_tile.x, self.game.chosen_tile.y)
                    self.game.get_game()
                else:
                    print("Doors Dont Align")

    def do_n(self, line):
        if self.game.state == "Moving":
            self.game.select_move(d.NORTH)
            self.game.get_game()

    def do_s(self, line):
        if self.game.state == "Moving":
            self.game.select_move(d.SOUTH)
            self.game.get_game()

    def do_e(self, line):
        if self.game.state == "Moving":
            self.game.select_move(d.EAST)
            self.game.get_game()

    def do_w(self, line):
        if self.game.state == "Moving":
            self.game.select_move(d.WEST)
            self.game.get_game()

    def do_draw(self):
        if self.game.state == "Drawing Card":
            self.game.draw_dev_card


if __name__ == "__main__":
    Commands().cmdloop()
