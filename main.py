import shelve
import cmd
import sys
import os
from classes.directions import Direction as d
from classes.game import Game
from classes.player import Player
from classes.tile import *
from classes.difficulty import *
from classes.controller import Controller


class Commands(cmd.Cmd):
    intro = (
        "Welcome, type help or ? to list the commands "
        "or 'start' to start the game"
    )

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = ">> "
        # self.player = Player()
        # self.game = Game(self.player)
        self.controller = Controller()
        if len(sys.argv) > 1:
            try:
                self.do_load(sys.argv[1])
            except Exception:
                print("File not found")

    def get_game(self):
        return self.controller.get_game()

    def do_start(self, line):
        """
        Starts a new game

        Required state: Starting

        Syntax: start
        """
        self.controller.start(line)

    def do_difficulty(self, line):
        """
        Selects the games difficulty

        Required State: Choosing Difficulty

        Syntax: difficulty <difficulty>
        """
        this_line = line.lower().strip()
        self.controller.difficulty(this_line)

    def do_rotate(self, line):
        """
        Rotates the current map piece 1 rotation clockwise

        Required state: Rotating

        Syntax: rotate
        """
        self.controller.rotate(line)

    def do_place(self, line):
        """
        Places the current map tile

        Required state: Rotating

        Syntax: place
        """
        self.controller.place(line)

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
        self.controller.choose(direction)

    def do_n(self, line):
        """
        Moves the player to the North tile

        Required state: Moving

        Syntax: n
        """
        self.controller.n(line)

    def do_s(self, line):
        """
        Moves the player to the South tile

        Required state: Moving

        Syntax: s
        """
        self.controller.s(line)

    def do_e(self, line):
        """
        Moves the player to the East tile

        Required state: Moving

        Syntax: e
        """
        self.controller.e(line)

    def do_w(self, line):
        """
        Moves the player to the West tile

        Required state: Moving

        Syntax: w
        """
        self.controller.w(line)

    def do_save(self, name):
        """
        Takes a filepath and saves the game to a file

        Required state: any

        Syntax: save <filepath>
        """
        self.controller.save(name)

    def do_load(self, name):
        """
        Takes a filepath and loads the game from a file

        Required state: any

        Syntax: load <filepath>
        """
        self.controller.load(name)

    def do_restart(self, line):
        """
        Deletes your current progress and restarts the game

        Required state: any

        Syntax: restart
        """
        self.controller.restart(line)

    def do_attack(self, line):
        """
        The player attacks the zombies, optionaly with items or weapons

        Required state: Attacking

        Syntax:
            attack
            attack <item>
            attack <item>, <item>
        """
        self.controller.attack(line)

    def do_use(self, line):
        """
        The player uses their items

        Required state: Moving

        Syntax:
            use
            use <item>
            use <item>, <item>
        """
        self.controller.use(line)

    def do_drop(self, item):
        """
        Drops an item from your inventory

        Required state: any

        Syntax: drop <item>
        """
        self.controller.drop(item)

    def do_swap(self, line):
        """
        Swaps an item in you hand with the one in the room

        Required state: Swapping Item

        Syntax: swap <item>
        """
        self.controller.swap(line)

    def do_draw(self, line):
        """
        Draws a new development card (Must be done after evey move)

        Required state: Drawing Dev Card

        Syntax: draw
        """
        self.controller.draw(line)

    def do_run(self, direction):
        """
        Flee from zombies in a specific direction, lose 1 health

        Required state: Attacking

        Syntax: run <direction>
        """
        direction = direction.lower().strip()
        self.controller.run(direction)

    def do_cower(self, line):
        """
        Cower in a room. Gain 3 health but lose time

        Required state: Moving

        Syntax: cower
        """
        self.controller.cower(line)

    def do_search(self, line):
        """
        Search for the zombie totem. (Player must be in the evil temple)

        Required state: Moving

        Syntax: search
        """
        self.controller.search(line)

    def do_bury(self, line):
        """
        Buries the totem. (Player must be in the graveyard)

        Required state: Moving

        Syntax: bury
        """
        self.controller.bury(line)

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
        self.controller.status(line)


if __name__ == "__main__":
    try:
        Commands().cmdloop()
    except Exception as e:
        print(e)
        print("Something went wrong, please restart")
