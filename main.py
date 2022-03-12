import random
from directions import Direction as d
import pandas as pd
import cmd


class Game:
    def __init__(self, player, time=9, game_map=None, indoor_tiles=None, outdoor_tiles=None, chosen_tile=None,
                 dev_cards=None, state="Starting", current_move_direction=None):
        if indoor_tiles is None:
            indoor_tiles = []  # Will contain a list of all available indoor tiles
        if outdoor_tiles is None:
            outdoor_tiles = []  # Will contain a list of all available outdoor tiles
        if dev_cards is None:
            dev_cards = []  # Will contain a list of all available development cards
        if game_map is None:
            game_map = {}  # Tiles dictionary will have the x and y co-ords as the key and the Tile object as the value
        self.player = player
        self.time = time
        self.indoor_tiles = indoor_tiles
        self.outdoor_tiles = outdoor_tiles
        self.dev_cards = dev_cards
        self.tiles = game_map
        self.chosen_tile = chosen_tile
        self.state = state
        self.current_move_direction = current_move_direction
        self.current_zombies = 0

    def start_game(self):
        self.load_tiles()
        for tile in self.indoor_tiles:
            if tile.name == 'Foyer':  # Game always starts in the Foyer at 16,16
                self.chosen_tile = tile
                self.state = "Rotating"
                break

    def get_game(self):
        print(self.tiles)
        return print(f'the player is at {self.player.get_x(), self.player.get_y()}'
                     f' the chosen tile is {self.chosen_tile.name}, {self.chosen_tile.doors}'
                     f' the state is {self.state} ENTRANCE {self.chosen_tile.entrance}')

    # Loads tiles from excel file
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
            if len(self.indoor_tiles) == 0:
                return print("No more indoor tiles")
            if self.get_current_tile().name == "Dining Room" \
                    and self.current_move_direction == self.get_current_tile().entrance:
                t = [t for t in self.outdoor_tiles if t.name == "Patio"]
                tile = t[0]
                tile.set_x(x)
                tile.set_y(y)
                self.chosen_tile = tile
            else:
                tile = random.choice(self.indoor_tiles)  # Chooses a random indoor tile and places it
                tile.set_x(x)
                tile.set_y(y)
                self.chosen_tile = tile
        elif self.get_current_tile().type == "Outdoor":
            if len(self.outdoor_tiles) == 0:
                return print("No more outdoor tiles")
            tile = random.choice(self.outdoor_tiles)
            tile.set_x(x)
            tile.set_y(y)
            self.chosen_tile = tile

    # Loads development cards from excel file
    def load_dev_cards(self):
        card_data = pd.read_excel('DevCards.xlsx')
        for card in card_data.iterrows():
            item = card[1][0]
            event_one = (card[1][1], card[1][2])
            event_two = (card[1][3], card[1][4])
            event_three = (card[1][5], card[1][6])
            dev_card = DevCard(item, event_one, event_two, event_three)
            self.dev_cards.append(dev_card)
        random.shuffle(self.dev_cards)

    def move_player(self, x, y):
        self.player.set_y(y)
        self.player.set_x(x)
        self.state = "Moving"  # State should be drawing card

    def get_tile_at(self, x, y):
        return self.tiles[(x, y)]

    def select_move(self, direction):
        x, y = self.get_destination_coords(direction)
        if self.check_for_door(direction):  # If there's a door where the player tried to move
            self.current_move_direction = direction
            if self.check_for_room(x, y) is False:
                self.draw_tile(x, y)
                self.state = "Rotating"
            if self.check_for_room(x, y):
                if self.check_indoor_outdoor_move(self.get_current_tile().type, self.get_tile_at(x, y).type):
                    return print("Cannot Move this way")
                else:
                    self.move_player(x, y)

    def check_indoor_outdoor_move(self, current_type, move_type):
        if current_type != move_type and self.get_current_tile().name != "Patio" or "Dining Room":
            return False

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

    def check_entrances_align(self):
        if self.get_current_tile().entrance == d.NORTH:
            if self.chosen_tile.entrance == d.SOUTH:
                return True
        if self.get_current_tile().entrance == d.SOUTH:
            if self.chosen_tile.entrance == d.NORTH:
                return True
        if self.get_current_tile().entrance == d.WEST:
            if self.chosen_tile.entrance == d.EAST:
                return True
        if self.get_current_tile().entrance == d.EAST:
            if self.chosen_tile.entrance == d.WEST:
                return True
        return print("Entrances Dont Align")

    def check_dining_room_has_exit(self):
        tile = self.chosen_tile
        if tile.name == "Dining Room":
            if self.current_move_direction == d.NORTH and tile.entrance == d.SOUTH:
                return False
            if self.current_move_direction == d.SOUTH and tile.entrance == d.NORTH:
                return False
            if self.current_move_direction == d.EAST and tile.entrance == d.WEST:
                return False
            if self.current_move_direction == d.WEST and tile.entrance == d.EAST:
                return False
        else:
            return True

    def place_tile(self, x, y):
        tile = self.chosen_tile
        self.tiles[(x, y)] = tile
        self.state = "Moving"
        if tile.type == "Outdoor":
            self.outdoor_tiles.pop(self.outdoor_tiles.index(tile))
        elif tile.type == "Indoor":
            self.indoor_tiles.pop(self.indoor_tiles.index(tile))

    def get_current_tile(self):  # returns the current tile that the player is at
        return self.tiles[self.player.get_x(), self.player.get_y()]

    def rotate(self):
        tile = self.chosen_tile
        tile.rotate_tile()
        if tile.name == "Foyer":
            return
        if self.get_current_tile().name == "Dining Room" or "Patio":
            tile.rotate_entrance()

    # Call when player enters a room and draws a dev card
    def trigger_dev_card(self, time):
        if len(self.dev_cards) == 0:
            self.lose_game()
            return
        dev_card = self.dev_cards[0]
        self.dev_cards.pop(0)
        event = dev_card.get_event_at_time(time)  # Gets the event at the current time
        if event[0] == "Nothing":
            print("There is nothing in this room")
            return
        elif event[0] == "Health":  # Change health of player
            print("There might be something in this room")
            self.player.add_health(event[1])
            if event[1] > 0:
                print(f"You gained {event[1]} health")
            elif event[1] < 0:
                print(f"You lost {event[1]} health")
                if self.player.get_health() <= 0:
                    self.lose_game()
                    return
            elif event[1] == 0:
                print("You didn't gain or lose any health")
        elif event[0] == "Item":  # Add item to player's inventory if there is room
            next_card = self.dev_cards[0]
            print(f"There is an item in this room: {next_card.get_item()}")
            if len(self.player.get_items()) < 2:
                self.dev_cards.pop(0)
                self.player.add_item(next_card.get_item())
                print(f"You picked up the {next_card.get_item()}")
            else:
                print("You already have two items, do you want to drop one of them?")
                self.state = "Dropping Item"  # Create CMD for dropping item
        elif event[0] == "Zombies":  # Add zombies to the game, begin combat
            print(f"There are {event[1]} zombies in this room, prepare to fight!")
            self.current_zombies = int(event[1])
            self.state = "Attacking"  # Create CMD for attacking zombies
    
    # Call in CMD if state is attacking, *items is a list of items the player is going to use
    def trigger_attack(self, *item):
        player_attack = self.player.get_attack()
        zombies = self.current_zombies
        
        if len(item) == 2:  # If the player is using two items
            if "Oil" in item and "Candle" in item:
                print("You used the oil and the candle to attack the zombies, it kills all of them")
                self.player.remove_item("Oil")
                return
            elif "Gasoline" in item and "Candle" in item:
                print("You used the gasoline and the candle to attack the zombies, it kills all of them")
                self.player.remove_item("Gasoline")
                return
            elif "Gasoline" in item and "Chainsaw" in item:
                #Add uses to chainsaw
                self.player.remove_item("Gasoline")
        elif len(item) == 1:
            if item == "Machete":
                self.player.add_attack(2)
            elif item == "Chainsaw":
                self.player.add_attack(3)
            elif item == "Golf Club" or item == "Grisly Femur" or item == "Board With Nails":
                self.player.add_attack(1)
            elif item == "Can of Soda":
                self.player.add_health(2)
            elif item == "Oil":
                self.trigger_run(0)
                return

        # Calculate damage on the player
        damage = zombies - player_attack
        print(f"You attacked the zombies, you lost {damage} health")
        self.player.add_health(-damage)
        if self.player.get_health() <= 0:
            self.lose_game()
            return
        else:
            self.current_zombies = 0
            self.state = "Moving"

    # DO MOVEMENT INTO ROOM, Call if state is attacking and player wants to run away
    def trigger_run(self, health_lost = -1):
        self.state = "Moving"
        self.player.add_health(health_lost)
        print(f"You run away from the zombies, and lose {health_lost} health")
    
    # If player chooses to cower in stead of move to a new room
    def trigger_cower(self):
        self.player.add_health(3)
        self.dev_cards.pop(0)
        print("You cower in fear, gaining 3 health, but lose time with the dev card")

    # Call when player wants to drop an item, and state is dropping item
    def drop_item(self, old_item, new_item):
        self.player.remove_item(old_item)
        self.player.add_item(new_item)
        print(f"You dropped the {old_item} and picked up the {new_item}")

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

    def lose_game(self):
        print("You lose")


class Player:
    def __init__(self, attack=1, health=6, x=16, y=16):
        self.attack = attack
        self.health = health
        self.x = x  # x Will represent the players position horizontally starts at 16
        self.y = y  # y will represent the players position vertically starts at 16
        self.items = []  # Holds the players items. Can hold 2 items at a time

    def get_health(self):
        return self.health

    def get_attack(self):
        return self.attack

    def set_attack(self, attack):
        self.attack = attack

    def set_health(self, health):
        self.health = health
    
    def add_health(self, health):
        self.health += health

    def add_attack(self, attack):
        self.attack += attack

    def get_items(self):
        return self.items
    
    def add_item(self, item):
        if len(self.items) < 2:
            self.items.append(item)
    
    def remove_item(self, item):
        self.items.pop(self.items.index(item))

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


# Development cards for the game. Played when the player moves into the room.
class DevCard:
    def __init__(self, item, event_one, event_two, event_three):
        self.item = item
        self.event_one = event_one
        self.event_two = event_two
        self.event_three = event_three

    def get_event_at_time(self, time):
        if time == 9:
            return self.event_one
        elif time == 10:
            return self.event_two
        elif time == 11:
            return self.event_three
    
    def get_item(self):
        return self.item

    def __str__(self):
        return "Item: {}, Event 1: {}, Event 2: {}, Event 3: {}".format(self.item, self.event_one, self.event_two, self.event_three)


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
            return
        if self.entrance == d.SOUTH:
            self.set_entrance(d.WEST)
            return
        if self.entrance == d.EAST:
            self.set_entrance(d.SOUTH)
            return
        if self.entrance == d.WEST:
            self.set_entrance(d.NORTH)
            return

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
    intro = 'Welcome, type help or ? to list the commands '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.player = Player()
        self.game = Game(self.player)

    def do_start(self, line):
        """Starts a new game"""
        if self.game.state == "Starting":
            self.game.start_game()
            self.game.get_game()
        else:
            print("Game has already Started")

    def do_rotate(self, line):
        """Rotates the current map piece 1 rotation clockwise"""
        if self.game.state == "Rotating":
            self.game.rotate()
            self.game.get_game()
        else:
            print("Tile not chosen to rotate")

    def do_place(self, line):
        """Places the current map tile"""
        if self.game.state == "Rotating":
            if self.game.chosen_tile.name == "Foyer":
                self.game.place_tile(16, 16)
                self.game.get_game()
            elif self.game.check_dining_room_has_exit() is False:
                return print("Dining room entrance must face an empty tile")
            else:
                if self.game.get_current_tile().name == "Dining Room" \
                        and self.game.current_move_direction == self.game.get_current_tile().entrance:
                    if self.game.check_entrances_align():
                        self.game.place_tile(self.game.chosen_tile.x, self.game.chosen_tile.y)
                        self.game.move_player(self.game.chosen_tile.x, self.game.chosen_tile.y)
                        self.game.get_game()
                elif self.game.check_doors_align(self.game.current_move_direction):
                    self.game.place_tile(self.game.chosen_tile.x, self.game.chosen_tile.y)
                    self.game.move_player(self.game.chosen_tile.x, self.game.chosen_tile.y)
                    self.game.get_game()
                else:
                    print("Doors Dont Align")
        else:
            print("Tile not chosen to place")

    def do_n(self, line):
        """Moves the player North"""
        if self.game.state == "Moving":
            self.game.select_move(d.NORTH)
            self.game.get_game()
        else:
            print("Player not ready to move")

    def do_s(self, line):
        """Moves the player South"""
        if self.game.state == "Moving":
            self.game.select_move(d.SOUTH)
            self.game.get_game()
        else:
            print("Player not ready to move")

    def do_e(self, line):
        """Moves the player East"""
        if self.game.state == "Moving":
            self.game.select_move(d.EAST)
            self.game.get_game()
        else:
            print("Player not ready to move")

    def do_w(self, line):
        """Moves the player West"""
        if self.game.state == "Moving":
            self.game.select_move(d.WEST)
            self.game.get_game()
        else:
            print("Player not ready to move")

    def do_save(self, line):
        """Takes a filepath and saves the game to a file"""
        pass

    def do_load(self, line):
        """Takes a filepath and loads the game from a file"""
        pass

    def do_restart(self, line):
        """Deletes your progress and ends the game"""
        del self.game
        del self.player
        self.player = Player()
        self.game = Game(self.player)

    def do_draw(self):
        """Draws a new development card (Must be done after evey move)"""
        if self.game.state == "Drawing Card":
            self.game.draw_dev_card


if __name__ == "__main__":
    Commands().cmdloop()
