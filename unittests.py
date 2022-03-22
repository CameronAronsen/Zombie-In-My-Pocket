import shelve
import unittest
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
        game_shelve = shelve.open("./saves/test_move.db")
        save = game_shelve['game']
        self.game = save
        game_shelve.close()
        print(self.game.player.get_x())

    def test_player_moves_north(self):
        self.assertEqual(1, 1)

class TestPlayerAttacks(unittest.TestCase):

    def test_player_attacks(self):
        self.assertEqual(1, 1)

if __name__ == "__main__":
    unittest.main()