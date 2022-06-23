import shelve
import cmd
import sys
import os
from classes.directions import Direction as d
from classes.game import Game
from classes.player import Player
from classes.tile import *
from classes.difficulty import *


class Controller():
    def __init__(self):
        self.player = Player()
        self.game = Game(self.player)

    def get_game(self):
        return self.game

    def start(self, line):
        if self.game.state == "Starting":
            print("Starting new game...")
            print("Dont worry if it is taking a while to load")
            self.game.start_game()
            self.game.get_game()
        else:
            print("Game has already Started")

    def difficulty(self, line):
        if self.game.state == "Choosing Difficulty":
            if line == "easy":
                self.game.get_player().set_difficulty(EasyDifficulty(self.game))
                self.game.get_player().trigger_difficulty()
            elif line == "medium":
                self.game.get_player().set_difficulty(MediumDifficulty(self.game))
                self.game.get_player().trigger_difficulty()
            else:
                self.game.get_player().set_difficulty(HardDifficulty(self.game))
                self.game.get_player().trigger_difficulty()
            self.game.state = "Rotating"
            self.game.get_game()
        else:
            print("Cannot Set Difficulty Right Now")

    def rotate(self, line):
        if self.game.state == "Rotating":
            self.game.rotate()
            self.game.get_game()
        else:
            print("Tile not chosen to rotate")

    def place(self, line):
        if self.game.state == "Rotating":
            if self.game.chosen_tile.name == "Foyer":
                self.game.place_tile(16, 16)
            elif self.game.check_dining_room_has_exit() is False:
                return print("Dining room entrance must face an empty tile")
            else:
                if (
                    self.game.get_current_tile().name == "Dining Room" and
                    self.game.current_move_direction ==
                    self.game.get_current_tile().entrance
                ):
                    if self.game.check_entrances_align():
                        self.game.place_tile(
                            self.game.chosen_tile.x, self.game.chosen_tile.y
                        )
                        self.game.move_player(
                            self.game.chosen_tile.x, self.game.chosen_tile.y
                        )
                elif self.game.check_doors_align(
                    self.game.current_move_direction
                ):
                    self.game.place_tile(
                        self.game.chosen_tile.x, self.game.chosen_tile.y
                    )
                    self.game.move_player(
                        self.game.chosen_tile.x, self.game.chosen_tile.y
                    )
                else:
                    print(
                        "Must have at least one door facing "
                        "the way you came from"
                    )
            self.game.increment_player_moves()
            self.game.update_tiles_placed()
            self.game.get_game()
        else:
            print("Tile not chosen to place")

    def choose(self, direction):
        if direction == "n":
            direction = d.NORTH
        if direction == "e":
            direction = d.EAST
        if direction == "s":
            direction = d.SOUTH
        if direction == "w":
            direction = d.WEST
        if self.game.state == "Choosing Door":
            self.game.can_cower = False
            self.game.choose_door(direction)
        else:
            print("Cannot choose a door right now")

    def n(self, line):
        if self.game.state == "Moving":
            self.game.select_move(d.NORTH)
            self.game.set_last_room("n")
            self.game.update_player_move()
            self.game.get_game()
        else:
            print("Player not ready to move")

    def s(self, line):
        if self.game.state == "Moving":
            self.game.select_move(d.SOUTH)
            self.game.set_last_room("s")
            self.game.update_player_move()
            self.game.get_game()
        else:
            print("Player not ready to move")

    def e(self, line):
        if self.game.state == "Moving":
            self.game.select_move(d.EAST)
            self.game.set_last_room("e")
            self.game.update_player_move()
            self.game.get_game()
        else:
            print("Player not ready to move")

    def w(self, line):
        if self.game.state == "Moving":
            self.game.select_move(d.WEST)
            self.game.set_last_room("w")
            self.game.update_player_move()
            self.game.get_game()
        else:
            print("Player not ready to move")

    def save(self, name):
        if not name:
            return print("Must enter a valid file name")
        else:
            name = name.lower().strip()
            file_name = name + ".db"
            game_shelve = shelve.open("./saves/" + file_name)
            game_shelve["game"] = self.game
            self.game.get_game()
            game_shelve.close()

    def load(self, name):
        if not name:
            return print("Must enter a valid file name")
        else:
            name = name.lower().strip()
            file_name = name + ".db"
            try:
                file_exists = os.path.exists("./saves/" + file_name + ".dat")
                if not file_exists:
                    raise FileNotFoundError
                game_shelve = shelve.open("./saves/" + file_name)
                save = game_shelve["game"]
                self.game = save
                self.game.get_game()
                game_shelve.close()
            except FileNotFoundError:
                print(f"No File with this name, {file_name} exists")

    def restart(self, line):
        del self.game
        del self.player
        self.player = Player()
        self.game = Game(self.player)

    def attack(self, line):
        arg1 = ""
        arg2 = None
        if "," in line:
            arg1, arg2 = [item for item in line.split(", ")]
        else:
            arg1 = line

        player_items = self.game.get_player().get_items()
        item_names = [item[0] for item in player_items]
        if self.game.state == "Attacking":
            if arg1 == "":
                self.game.trigger_attack()
            elif arg2 is None:
                if arg1.title() in item_names:
                    self.game.trigger_attack(arg1.lower().strip())
            elif arg1 != "" and arg2 is not None:
                if arg1.title() in item_names and arg2.title() in item_names:
                    self.game.trigger_attack(
                        arg1.lower().strip(), arg2.lower().strip()
                    )
            self.game.update_attacks()
            if (
                len(self.game.chosen_tile.doors) == 1 and
                self.game.chosen_tile.name != "Foyer"
            ):
                self.game.state = "Choosing Door"
                self.game.get_game()
            if self.game.state == "Game Over":
                print(
                    "You lose, game over, you have "
                    "succumbed to the zombie horde"
                )
                print("To play again, type 'restart'")
                self.game.lose_game()
            else:
                self.game.get_game()
        else:
            print("You cannot attack right now")

    def use(self, line):
        arg1 = ""
        arg2 = None
        if "," in line:
            arg1, arg2 = [item for item in line.split(", ")]
        else:
            arg1 = line

        player_items = self.game.get_player().get_items()
        item_names = [item[0] for item in player_items]
        if self.game.state == "Moving":
            if arg1 == "":
                return
            if arg2 is None:
                if arg1.title() in item_names:
                    self.game.use_item(arg1.lower().strip())
                else:
                    print("That item is not in you inventory")
            elif arg1 != "" and arg2 is not None:
                if arg1.title() in item_names and arg2.title() in item_names:
                    self.game.use_item(
                        arg1.lower().strip(), arg2.lower().strip()
                    )
                else:
                    print("That item is not in you inventory")
        else:
            print("You cannot do that right now")

    def drop(self, item):
        player_items = self.game.get_player().get_items()
        item_names = [item[0] for item in player_items]
        if self.game.state != "Game Over":
            if item.title() in item_names:
                self.game.drop_item(item.lower().strip())
                self.game.get_game()
            else:
                print("That item is not in your inventory")

    def swap(self, line):
        player_items = self.game.get_player().get_items()
        item_names = [item[0] for item in player_items]
        if self.game.state == "Swapping Item":
            if line.title() in item_names:
                self.game.drop_item(line.lower().strip())
                self.game.get_player().add_item(
                    self.game.room_item[0], self.game.room_item[1]
                )
                self.game.room_item = None
                self.game.get_game()
            else:
                print("That item is not in your inventory, try again")

    def draw(self, line):
        if self.game.state == "Drawing Dev Card":
            self.game.update_dev_cards_used()
            self.game.trigger_dev_card(self.game.time)
        else:
            print("Cannot currently draw a card")

    def run(self, direction):
        direction = direction.lower().strip()
        if self.game.state == "Attacking":
            if direction == "n":
                self.game.trigger_run(d.NORTH)
            elif direction == "e":
                self.game.trigger_run(d.EAST)
            elif direction == "s":
                self.game.trigger_run(d.SOUTH)
            elif direction == "w":
                self.game.trigger_run(d.WEST)
            else:
                print("Cannot run that direction")
            if (
                len(self.game.get_current_tile().doors) == 1 and
                self.game.chosen_tile.name != "Foyer"
            ):
                self.game.state = "Choosing Door"
                self.game.get_game()
        else:
            print("Cannot run when not being attacked")
        self.game.get_game()

    def cower(self, line):
        if self.game.state == "Moving":
            self.game.trigger_cower()
        else:
            print("Cannot cower while right now")

    def search(self, line):
        if line == "testing":  # Used for testing
            self.game.search_for_totem(True)
        if self.game.state == "Moving":
            self.game.search_for_totem()
        else:
            print("Cannot search currently")

    def bury(self, line):
        if self.game.state == "Moving":
            if line == "testing":
                self.game.bury_totem(True)
            else:
                self.game.bury_totem(False)
        else:
            print("Cannot currently bury the totem")

    def prompt(self, line):
        self.prompt = line + ' '

    def exit(self, line):
        return True

    def status(self, line):
        if (
            len(self.game.tiles) != 0 and
            self.game.state != "Game Over" or
            self.game.state != "Starting"
        ):
            self.game.get_player_status()
        else:
            print("Cannot show status at this time")
