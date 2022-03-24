import random
import pandas as pd
from classes.directions import Direction as d
from classes.player import Player
from classes.devcard import DevCard
from classes.tile import *
from classes.database import Database
from classes.finish_menu import FinishScreen


class Game:
    """
    >>> from classes.game import Game
    >>> from classes.player import Player
    >>> from classes.tile import *
    >>> from classes.database import Database
    >>> from classes.devcard import DevCard
    >>> from classes.directions import Direction as d
    >>> player = Player()
    >>> game = Game(player)
    >>> game.start_game()
    >>> game.get_time()
    9
    >>> game.place_tile(16, 16)
    >>> game.check_for_room(16, 16)
    True

    """
    def __init__(
        self,
        player,
        time=9,
        game_map=None,
        indoor_tiles=None,
        outdoor_tiles=None,
        chosen_tile=None,
        dev_cards=None,
        state="Starting",
        current_move_direction=None,
        can_cower=True,
    ):
        if indoor_tiles is None:
            indoor_tiles = (
                []
            )  # Will contain a list of all available indoor tiles
        if outdoor_tiles is None:
            outdoor_tiles = (
                []
            )  # Will contain a list of all available outdoor tiles
        if dev_cards is None:
            dev_cards = (
                []
            )  # Will contain a list of all available development cards
        if game_map is None:
            game_map = {}  # Tiles dictionary will have the x and y co-ords
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
        self.can_cower = can_cower
        self.room_item = None
        self.last_room = None
        self.dev_cards_used = 0
        self.tiles_placed = 0
        self.attack_count = 0

    #  Run to initialise the game
    def start_game(self):
        self.database = Database()
        self.load_tiles()
        self.load_dev_cards()
        self.database.close_connection()
        del self.database
        for tile in self.indoor_tiles:
            if (
                tile.name == "Foyer"
            ):  # Game always starts in the Foyer at 16,16
                self.chosen_tile = tile
                self.state = "Rotating"
                break

    def get_game(self):
        s = ""
        f = ""
        if self.state == "Moving":
            s = (
                "In this state you are able to move the player "
                "using the movement commands of n, e, s, w"
            )
        if self.state == "Rotating":
            s = (
                "Use the rotate command to rotate tiles and align doors,"
                " Once you are happy with the door position"
                " you can place the tile with the place command"
            )
        if self.state == "Choosing Door":
            s = (
                "Choose where to place a new door"
                " with the choose command + n, e, s, w"
            )
        if self.state == "Drawing Dev Card":
            s = "Use the draw command to draw a random development card"
        for door in self.chosen_tile.doors:
            f += door.name + ", "
        return print(
            f"The chosen tile "
            f"is {self.chosen_tile.name}, the available doors "
            f"in this room are {f}\n "
            f"The state is {self.state}. {s}\n "
            f"Special Entrances : {self.chosen_tile.entrance}"
        )

    def get_player_status(self):
        return print(
            f"--------------------------------------"
            f"--------------------------------------\n"
            f"Game Status \n"
            f"--------------------------------------"
            f"--------------------------------------\n"
            f"It is {self.get_time()} pm \n"
            f"Holding totem: {self.player.get_totem()} \n"
            f"--------------------------------------"
            f"--------------------------------------\n"
            f"The player currently has {self.player.get_health()} health \n"
            f"The player currently has {self.player.get_attack()} attack \n"
            f"The players items are {self.player.get_items()} "
            f"(Item, Charges left)\n"
            f"--------------------------------------"
            f"--------------------------------------\n"
            f"The current tile is {self.get_current_tile().name} \n"
            f"There are currently {len(self.dev_cards)} development cards "
            f"left in the deck\n"
            f"The game state is {self.state}\n"
            f"--------------------------------------"
            f"--------------------------------------"
        )

    def get_time(self):
        return self.time

    def get_player(self):
        return self.player

    def get_player_x(self):
        return self.player.get_x()

    def get_player_y(self):
        return self.player.get_y()

    def get_player_moves(self):
        return self.player.get_move_count()

    def get_dev_cards_used(self):
        return self.dev_cards_used

    def get_tiles_placed(self):
        return self.tiles_placed

    def get_attacks_completed(self):
        return self.attack_count

    def update_player_move(self):
        self.player.increment_move_count()

    def update_tiles_placed(self):
        self.tiles_placed += 1

    def update_dev_cards_used(self):
        self.dev_cards_used += 1

    def update_attacks(self):
        self.attack_count += 1

    def set_last_room(self, direction):
        if direction == "n":
            self.last_room = d.SOUTH
        elif direction == "e":
            self.last_room = d.WEST
        elif direction == "s":
            self.last_room = d.NORTH
        elif direction == "w":
            self.last_room = d.EAST

    # Loads tiles from excel file
    def load_tiles(self):  # Needs Error handling in this method
        tiles = self.database.get_tiles()
        for tile in tiles:
            doors = self.resolve_doors(tile[4], tile[5], tile[6], tile[7])
            if tile[3] == "Outdoor":
                new_tile = OutdoorTile(tile[1], tile[2], doors)
                if tile[1] == "Patio":
                    new_tile.set_entrance(d.NORTH)
                self.outdoor_tiles.append(new_tile)
            if tile[3] == "Indoor":
                new_tile = IndoorTile(tile[1], tile[2], doors)
                if tile[1] == "Dining Room":
                    new_tile.set_entrance(d.NORTH)
                self.indoor_tiles.append(new_tile)
        random.shuffle(self.indoor_tiles)
        random.shuffle(self.outdoor_tiles)

    def draw_tile(
        self, x, y
    ):  # Called when the player moves through a door into room
        if self.get_current_tile().type == "Indoor":  # get a new tile
            if len(self.indoor_tiles) == 0:
                return print("No more indoor tiles")
            if (
                self.get_current_tile().name == "Dining Room" and
                self.current_move_direction ==
                self.get_current_tile().entrance
            ):
                t = [t for t in self.outdoor_tiles if t.name == "Patio"]
                tile = t[0]
                tile.set_x(x)
                tile.set_y(y)
                self.chosen_tile = tile
            else:
                tile = self.indoor_tiles[
                    0
                ]  # Chooses a random indoor tile and places it
                tile.set_x(x)
                tile.set_y(y)
                self.chosen_tile = tile
        elif self.get_current_tile().type == "Outdoor":
            if len(self.outdoor_tiles) == 0:
                return print("No more outdoor tiles")
            tile = self.outdoor_tiles[0]
            tile.set_x(x)
            tile.set_y(y)
            self.chosen_tile = tile

    # Loads development cards
    def load_dev_cards(self):
        dev_cards = self.database.get_dev_cards()
        for card in dev_cards:
            item = card[1]
            event_one = (card[2], card[3])
            event_two = (card[4], card[5])
            event_three = (card[6], card[7])
            charges = card[8]
            dev_card = DevCard(
                item, charges, event_one, event_two, event_three
            )
            self.dev_cards.append(dev_card)
        random.shuffle(self.dev_cards)
        self.dev_cards.pop(0)
        self.dev_cards.pop(0)

    def move_player(
        self, x, y
    ):  # Moves the player coordinates to the selected tile, changes state
        self.player.set_y(y)
        self.player.set_x(x)
        if self.state == "Running":
            self.state = "Moving"
        else:
            self.state = "Drawing Dev Card"

    def get_tile_at(self, x, y):  # Returns the tile given x and y coordinates
        return self.tiles[(x, y)]

    def select_move(
        self, direction
    ):  # Takes the player input and runs all checks to see if move is valid
        x, y = self.get_destination_coords(direction)
        if self.check_for_door(
            direction
        ):  # If there's a door where the player tried to move
            self.current_move_direction = direction
            if self.check_for_room(x, y) is False:
                if self.state == "Running":
                    return print("Can only run into a discovered room")
                else:
                    self.draw_tile(x, y)
                    self.state = "Rotating"
            if self.check_for_room(x, y):
                if self.check_indoor_outdoor_move(
                    self.get_current_tile().type, self.get_tile_at(x, y).type
                ):
                    return print("Cannot Move this way")
                else:
                    self.move_player(x, y)

    def check_indoor_outdoor_move(
        self, current_type, move_type
    ):  # Makes sure player can only move outside through
        if (
            current_type != move_type and
            self.get_current_tile().name != "Patio" or
            "Dining Room"
        ):  # the dining room
            return False

    def get_destination_coords(
        self, direction
    ):  # Gets the x and y value of the proposed move
        if direction == d.NORTH:
            return self.player.get_x(), self.player.get_y() - 1
        if direction == d.SOUTH:
            return self.player.get_x(), self.player.get_y() + 1
        if direction == d.EAST:
            return self.player.get_x() + 1, self.player.get_y()
        if direction == d.WEST:
            return self.player.get_x() - 1, self.player.get_y()

    def check_for_door(
        self, direction
    ):  # Takes a direction and checks if the current room has a door there
        if direction in self.get_current_tile().doors:
            return True
        else:
            return False

    def check_for_room(
        self, x, y
    ):  # Takes a move direction and checks if there is a room there
        if (x, y) not in self.tiles:
            return False
        else:
            self.chosen_tile = self.tiles[(x, y)]
            return True

    def check_doors_align(
        self, direction
    ):  # Makes sure when placing a tile that a door is facing the player
        if self.chosen_tile.name == "Foyer":  # Trying to come from
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

    def check_entrances_align(
        self,
    ):  # Makes sure the dining room and patio entrances align
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
        return print(" Dining room and Patio entrances dont align")

    def check_dining_room_has_exit(
        self,
    ):  # used to make sure the dining room exit is not facing existing door
        tile = self.chosen_tile
        if tile.name == "Dining Room":
            if (
                self.current_move_direction == d.NORTH and
                tile.entrance == d.SOUTH
            ):
                return False
            if (
                self.current_move_direction == d.SOUTH and
                tile.entrance == d.NORTH
            ):
                return False
            if (
                self.current_move_direction == d.EAST and
                tile.entrance == d.WEST
            ):
                return False
            if (
                self.current_move_direction == d.WEST and
                tile.entrance == d.EAST
            ):
                return False
        else:
            return True

    def place_tile(self, x, y):  # Places the tile into game map dictionary
        tile = self.chosen_tile
        self.tiles[
            (x, y)
        ] = tile  # The tile is stored as a tuple as the key of the dictionary
        self.state = "Moving"  # And the tile is stored as the value
        if tile.type == "Outdoor":
            self.outdoor_tiles.pop(self.outdoor_tiles.index(tile))
        elif tile.type == "Indoor":
            self.indoor_tiles.pop(self.indoor_tiles.index(tile))

    def get_current_tile(
        self,
    ):  # returns the current tile that the player is at
        return self.tiles[self.player.get_x(), self.player.get_y()]

    def rotate(
        self,
    ):  # Rotates a selected tile one position clockwise during Rotating state
        tile = self.chosen_tile
        tile.rotate_tile()
        if tile.name == "Foyer":
            return
        if self.get_current_tile().name == "Dining Room" or "Patio":
            tile.rotate_entrance()

    # Call when player enters a room and draws a dev card
    def trigger_dev_card(self, time):
        if len(self.dev_cards) == 0:
            if self.get_time() >= 11:
                print("You have run out of time")
                self.lose_game()
                return
            else:
                print("Reshuffling The Deck")
                self.database = Database()
                self.load_dev_cards()
                self.database.close_connection()
                del self.database
                self.time += 1

        dev_card = self.dev_cards[0]
        self.dev_cards.pop(0)
        event = dev_card.get_event_at_time(
            time
        )  # Gets the event at the current time
        if event[0] == "Nothing":
            print("There is nothing in this room")
            if (
                len(self.chosen_tile.doors) == 1 and
                self.chosen_tile.name != "Foyer"
            ):
                self.state = "Choosing Door"
                self.get_game()
                return
            else:
                self.state = "Moving"
                self.get_game()
            return
        elif event[0] == "Health":  # Change health of player
            print("There might be something in this room")
            health = int(event[1])
            self.player.add_health(health)

            if health > 0:
                print(f"You gained {health} health")
                self.state = "Moving"
            elif health < 0:
                print(f"You lost {health} health")
                self.state = "Moving"
                if self.player.get_health() <= 0:
                    self.lose_game()
                    return
            elif health == 0:
                print("You didn't gain or lose any health")
            if (
                len(self.chosen_tile.doors) == 1 and
                self.chosen_tile.name != "Foyer"
            ):
                self.state = "Choosing Door"
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
            else:
                self.state = "Moving"
                self.get_game()
        elif (
            event[0] == "Item"
        ):  # Add item to player's inventory if there is room
            if len(self.dev_cards) == 0:
                if self.get_time() >= 11:
                    print("You have run out of time")
                    self.lose_game()
                    return
                else:
                    print("Reshuffling The Deck")
                    self.load_dev_cards()
                    self.time += 1
            next_card = self.dev_cards[0]
            print(f"There is an item in this room: {next_card.get_item()}")
            if len(self.player.get_items()) < 2:
                self.dev_cards.pop(0)
                self.player.add_item(next_card.get_item(), next_card.charges)
                print(f"You picked up the {next_card.get_item()}")
                if (
                    len(self.chosen_tile.doors) == 1 and
                    self.chosen_tile.name != "Foyer"
                ):
                    self.state = "Choosing Door"
                    self.get_game()
                else:
                    self.state = "Moving"
                    self.get_game()
            else:
                self.room_item = [next_card.get_item(), next_card.charges]
                response = input(
                    "You already have two items, do you want to drop "
                    "one of them? (Y/N) "
                )
                if response == "Y" or response == "y":
                    self.state = "Swapping Item"
                else:  # If player doesn't want to drop item, just move on
                    self.state = "Moving"
                    self.room_item = None
                    self.get_game()
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
        elif event[0] == "Zombies":  # Add zombies to the game, begin combat
            print(
                f"There are {event[1]} zombies in this room, "
                f"prepare to fight!"
            )
            self.current_zombies = int(event[1])
            self.state = "Attacking"  # Create CMD for attacking zombies

    # Call if state is attacking, *items islist of items the player is using
    def trigger_attack(self, *item):
        player_attack = self.player.get_attack()
        zombies = self.current_zombies
        if len(item) == 2:  # If the player is using two items
            if "oil" in item and "candle" in item:
                print(
                    "You used the oil and the candle to attack the zombies, "
                    "it kills all of them"
                )
                self.drop_item("Oil")
                self.state = "Moving"
                return
            elif "gasoline" in item and "candle" in item:
                print(
                    "You used the gasoline and the candle to attack "
                    "the zombies, it kills all of them"
                )
                self.drop_item("Gasoline")
                self.state = "Moving"
                return
            elif "gasoline" in item and "chainsaw" in item:
                chainsaw_charge = self.player.get_item_charges("Chainsaw")
                self.player.set_item_charges("Chainsaw", chainsaw_charge + 2)
                player_attack += 3
                self.drop_item("Gasoline")
                self.player.use_item_charge("Chainsaw")
            else:
                print("These items cannot be used together, try again")
                return
        elif len(item) == 1:
            if "machete" in item:
                player_attack += 2
            elif "chainsaw" in item:
                if self.player.get_item_charges("Chainsaw") > 0:
                    player_attack += 3
                    self.player.use_item_charge("Chainsaw")
                else:
                    print("This item has no charges left")
            elif (
                "golf club" in item or
                "grisly femur" in item or
                "board with nails" in item
            ):
                player_attack += 1
            elif "can of soda" in item:
                self.player.add_health(2)
                self.drop_item("Can Of Soda")
                print("Used Can Of Soda, gained 2 health")
                return
            elif "oil" in item:
                direction = self.last_room
                self.trigger_run(direction, 0)
                return
            else:
                print("You cannot use this item right now, try again")
                return

        # Calculate damage on the player
        damage = zombies - player_attack
        if damage < 0:
            damage = 0
        print(f"You attacked the zombies, you lost {damage} health")
        self.can_cower = True
        self.player.add_health(-damage)
        if self.player.get_health() <= 0:
            self.lose_game()
            return
        else:
            self.current_zombies = 0
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
            self.state = "Moving"

    def trigger_run(self, direction, health_lost=-1):
        self.state = "Running"
        self.select_move(direction)
        if self.state == "Moving":
            self.player.add_health(health_lost)
            print(
                f"You run away from the zombies, "
                f"and lose {health_lost} health"
            )
            self.can_cower = True
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
        else:
            self.state = "Attacking"

    def trigger_room_effect(
        self, room_name
    ):  # Used for the Garden and Kitchen special room effects
        if room_name == "Garden":
            self.player.add_health(1)
            print(
                f"After ending your turn in the {room_name} "
                f"you have gained one health"
            )
            self.state = "Moving"
        if room_name == "Kitchen":
            self.player.add_health(1)
            print(
                f"After ending your turn in the {room_name} "
                f"you have gained one health"
            )
            self.state = "Moving"

    # If player chooses to cower instead of move to a new room
    def trigger_cower(self):
        if self.can_cower:
            self.player.add_health(3)
            self.dev_cards.pop(0)
            self.state = "Moving"
            print(
                "You cower in fear, gaining 3 health, "
                "but lose time with the dev card"
            )
        else:
            return print("Cannot cower during a zombie door attack")

    # Call when player wants to drop an item, and state is dropping item
    def drop_item(self, old_item):
        for item in self.player.get_items():
            if item[0] == old_item.title():
                self.player.remove_item(item)
                print(f"You dropped the {old_item.title()}")
                return
        print("That item is not in your inventory")

    def use_item(self, *item):
        if "can of soda" in item:
            self.player.add_health(2)
            self.drop_item("Can Of Soda")
            print("Used Can Of Soda, gained 2 health")
        elif "gasoline" in item and "chainsaw" in item:
            chainsaw_charge = self.player.get_item_charges("Chainsaw")
            self.player.set_item_charges("Chainsaw", chainsaw_charge + 2)
            self.drop_item("Gasoline")
        else:
            print("These items cannot be used right now")
            return

    def choose_door(
        self, direction
    ):  # used to select where a door will be made during a zombie door attack
        if direction in self.chosen_tile.doors:
            print("Choose a NEW door not an existing one")
            return False
        else:
            self.chosen_tile.doors.append(direction)
            self.current_zombies = 3
            print(
                f"{self.current_zombies} Zombies have appeared, "
                f"prepare for battle. Use the attack command to"
                f" fight or the run command to flee"
            )
            self.state = "Attacking"

    def search_for_totem(
        self, testing=False
    ):  # Used to search for a totem in the evil temple, will draw dev card
        if self.get_current_tile().name == "Evil Temple":
            if self.player.has_totem:
                print("player already has the totem")
                return
            elif testing:
                self.player.found_totem()
            else:
                self.trigger_dev_card(self.time)
                self.player.found_totem()
        else:
            print("You cannot search for a totem in this room")

    def bury_totem(self, testing):
        if self.get_current_tile().name == "Graveyard":
            if self.player.has_totem:
                self.trigger_dev_card(self.time)
                if self.player.health != 0:
                    print("You Won")
                    self.state = "Game Over"
                    if not testing:
                        finish_screen = FinishScreen(True, self)
                        finish_screen.start()
        else:
            print("Cannot bury totem here")

    def check_for_dead_player(self):
        if self.player.health <= 0:
            return True
        else:
            return False

    @staticmethod
    def resolve_doors(n, e, s, w):
        doors = []
        if n == "1":
            doors.append(d.NORTH)
        if e == "1":
            doors.append(d.EAST)
        if s == "1":
            doors.append(d.SOUTH)
        if w == "1":
            doors.append(d.WEST)
        return doors

    def lose_game(self):
        self.state = "Game Over"
        finish_screen = FinishScreen(False, self)
        finish_screen.start()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
