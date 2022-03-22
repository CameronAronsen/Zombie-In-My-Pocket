import shelve
import unittest
from main import Commands
from classes.directions import Direction as d
from classes.game import Game
from classes.player import Player
from classes.tile import *

class TestGameCreation(unittest.TestCase):
    
    def setUp(self):
        self.player = Player()
        self.game = Game(self.player)
        self.game.start_game()

    def test_GameCreation(self):
        self.assertEqual(1, 1)

class TestPlayerMovement(unittest.TestCase):

    def setUp(self):
        self.player = Player()
        self.game = Game(self.player)
        self.commands = Commands()
        self.commands.do_load("test_move")
        print(self.game.player.get_x())
        print(self.game.player.get_y())

    def test_player_moves_north(self):
        self.commands.do_n(None)
        self.commands.do_rotate(None)
        self.commands.do_rotate(None)
        self.commands.do_place(None)
        print(self.game.player.get_x())
        print(self.game.player.get_y())


class TestPlayerAttacks(unittest.TestCase):

    def test_player_attacks(self):
        self.assertEqual(1, 1)

if __name__ == "__main__":
    unittest.main()