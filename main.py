import shelve
import cmd
import sys
import os
from classes.directions import Direction as d
from classes.game import Game
from classes.player import Player
from classes.tile import *


class Commands(cmd.Cmd):
    intro = (
        "Welcome, type help or ? to list the commands "
        "or 'start' to start the game"
    )

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = ">> "
        self.player = Player()
        self.game = Game(self.player)
        if len(sys.argv) > 1:
            try:
                self.do_load(sys.argv[1])
            except Exception:
                print("File not found")

    def get_game(self):
        return self.game

    def do_start(self, line):
        """
        Starts a new game

        Required state: Starting

        Syntax: start
        """
        if self.game.state == "Starting":
            print("Starting new game...")
            print("Dont worry if it is taking a while to load")
            self.game.start_game()
            self.game.get_game()
        else:
            print("Game has already Started")

    def do_rotate(self, line):
        """
        Rotates the current map piece 1 rotation clockwise

        Required state: Rotating

        Syntax: rotate
        """
        if self.game.state == "Rotating":
            self.game.rotate()
            self.game.get_game()
        else:
            print("Tile not chosen to rotate")

    def do_place(self, line):
        """
        Places the current map tile

        Required state: Rotating

        Syntax: place
        """
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

    def do_choose(self, direction):
        """
        If there are no new doors, use this command to create a new exit

        Required state: Choosing Door

        Syntax: choose <direction>
        """
        valid_inputs = ["n", "e", "s", "w"]
        if direction not in valid_inputs:
            return print(
                "Input a valid direction. "
                "(Check choose help for more information)"
            )
        direction = direction.lower().strip()
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

    def do_n(self, line):
        """
        Moves the player to the North tile

        Required state: Moving

        Syntax: n
        """
        if self.game.state == "Moving":
            self.game.select_move(d.NORTH)
            self.game.set_last_room("n")
            self.game.update_player_move()
            self.game.get_game()
        else:
            print("Player not ready to move")

    def do_s(self, line):
        """
        Moves the player to the South tile

        Required state: Moving

        Syntax: s
        """
        if self.game.state == "Moving":
            self.game.select_move(d.SOUTH)
            self.game.set_last_room("s")
            self.game.update_player_move()
            self.game.get_game()
        else:
            print("Player not ready to move")

    def do_e(self, line):
        """
        Moves the player to the East tile

        Required state: Moving

        Syntax: e
        """
        if self.game.state == "Moving":
            self.game.select_move(d.EAST)
            self.game.set_last_room("e")
            self.game.update_player_move()
            self.game.get_game()
        else:
            print("Player not ready to move")

    def do_w(self, line):
        """
        Moves the player to the West tile

        Required state: Moving

        Syntax: w
        """
        if self.game.state == "Moving":
            self.game.select_move(d.WEST)
            self.game.set_last_room("w")
            self.game.update_player_move()
            self.game.get_game()
        else:
            print("Player not ready to move")

    def do_save(self, name):
        """
        Takes a filepath and saves the game to a file

        Required state: any

        Syntax: save <filepath>
        """
        if not name:
            return print("Must enter a valid file name")
        else:
            name = name.lower().strip()
            file_name = name + ".db"
            game_shelve = shelve.open("./saves/" + file_name)
            game_shelve["game"] = self.game
            self.game.get_game()
            game_shelve.close()

    def do_load(self, name):
        """
        Takes a filepath and loads the game from a file

        Required state: any

        Syntax: load <filepath>
        """
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

    def do_restart(self, line):
        """
        Deletes your current progress and restarts the game

        Required state: any

        Syntax: restart
        """
        del self.game
        del self.player
        self.player = Player()
        self.game = Game(self.player)

    def do_attack(self, line):
        """
        The player attacks the zombies, optionaly with items or weapons

        Required state: Attacking

        Syntax:
            attack
            attack <item>
            attack <item>, <item>
        """
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
            else:
                pass
        else:
            print("You cannot attack right now")

    def do_use(self, line):
        """
        The player uses their items

        Required state: Moving

        Syntax:
            use
            use <item>
            use <item>, <item>
        """
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

    def do_drop(self, item):
        """
        Drops an item from your inventory

        Required state: any

        Syntax: drop <item>
        """
        player_items = self.game.get_player().get_items()
        item_names = [item[0] for item in player_items]
        if self.game.state != "Game Over":
            if item.title() in item_names:
                self.game.drop_item(item.lower().strip())
                self.game.get_game()
            else:
                print("That item is not in your inventory")

    def do_swap(self, line):
        """
        Swaps an item in you hand with the one in the room

        Required state: Swapping Item

        Syntax: swap <item>
        """
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

    def do_draw(self, line):
        """
        Draws a new development card (Must be done after evey move)

        Required state: Drawing Dev Card

        Syntax: draw
        """
        if self.game.state == "Drawing Dev Card":
            self.game.update_dev_cards_used()
            self.game.trigger_dev_card(self.game.time)
        else:
            print("Cannot currently draw a card")

    def do_run(self, direction):
        """
        Flee from zombies in a specific direction, lose 1 health

        Required state: Attacking

        Syntax: run <direction>
        """
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

    def do_cower(self, line):
        """
        Cower in a room. Gain 3 health but lose time

        Required state: Moving

        Syntax: cower
        """
        if self.game.state == "Moving":
            self.game.trigger_cower()
        else:
            print("Cannot cower while right now")

    def do_search(self, line):
        """
        Search for the zombie totem. (Player must be in the evil temple)

        Required state: Moving

        Syntax: search
        """
        if line == "testing":  # Used for testing
            self.game.search_for_totem(True)
        if self.game.state == "Moving":
            self.game.search_for_totem()
        else:
            print("Cannot search currently")

    def do_bury(self, line):
        """
        Buries the totem. (Player must be in the graveyard)

        Required state: Moving

        Syntax: bury
        """
        if self.game.state == "Moving":
            if line == "testing":
                self.game.bury_totem(True)
            else:
                self.game.bury_totem(False)
        else:
            print("Cannot currently bury the totem")

    def do_prompt(self, line):
        """
        Change the interactive prompt

        Required state: any

        Syntax: prompt <new prompt>
        """
        self.prompt = line + ' '

    def do_exit(self, line):
        """
        Exits the game without saving

        Required state: any

        Syntax: exit
        """
        return True

    def do_status(self, line):
        """
        Shows the status of the player, including time, health, and items

        Required state: any

        Syntax: status
        """
        if (
            len(self.game.tiles) != 0 and
            self.game.state != "Game Over" or
            self.game.state != "Starting"
        ):
            self.game.get_player_status()
        else:
            print("Cannot show status at this time")


if __name__ == "__main__":
    try:
        Commands().cmdloop()
    except Exception as e:
        print(e)
        print("Something went wrong, please restart")
