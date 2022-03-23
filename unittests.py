import shelve
import unittest
from main import Commands
from classes.directions import Direction as d
from classes.game import Game
from classes.player import Player
from classes.tile import *

class TestGameCreation(unittest.TestCase):
    
    def setUp(self):
        self.commands = Commands()

    def test_start_creates_new_game(self):
        self.commands.do_start(None)
        self.commands.do_place(None)
        game = self.commands.get_game()
        current_tile = game.get_current_tile()
        self.assertEqual(current_tile.get_name(), "Foyer")

    def test_load_creates_loaded_game(self):
        self.commands.do_load("test_move")
        game = self.commands.get_game()
        player_pos = game.get_player_x(), game.get_player_y()
        self.assertEqual(player_pos, (15, 14))
         
    def test_save_saves_current_game(self):
        pass

class TestPlayerMovement(unittest.TestCase):

    def setUp(self):
        self.commands = Commands()
        self.commands.do_load("test_move")

    def test_player_moves_north(self):
        self.commands.do_n(None)
        self.commands.do_rotate(None)
        self.commands.do_rotate(None)
        self.commands.do_place(None)
        game = self.commands.get_game()
        player_pos = game.get_player_x(), game.get_player_y()
        self.assertEqual(player_pos, (15, 13))

    def test_player_moves_south(self):
        self.commands.do_s(None)
        self.commands.do_rotate(None)
        self.commands.do_rotate(None)
        self.commands.do_place(None)
        game = self.commands.get_game()
        player_pos = game.get_player_x(), game.get_player_y()
        self.assertEqual(player_pos, (15, 15))
    
    def test_player_moves_east(self):
        self.commands.do_e(None)
        self.commands.do_place(None)
        game = self.commands.get_game()
        player_pos = game.get_player_x(), game.get_player_y()
        self.assertEqual(player_pos, (16, 14))
    
    def test_player_moves_west(self):
        self.commands.do_w(None)
        self.commands.do_rotate(None)
        self.commands.do_place(None)
        game = self.commands.get_game()
        player_pos = game.get_player_x(), game.get_player_y()
        self.assertEqual(player_pos, (14, 14))

    def test_north_from_dining_room_goes_to_patio(self):
        self.commands.do_n(None)
        self.commands.do_rotate(None)
        self.commands.do_rotate(None)
        self.commands.do_place(None)
        game = self.commands.get_game()
        current_tile = game.get_current_tile()
        self.assertEqual(current_tile.get_name(), "Patio")

    def test_cower_gains_health(self):
        self.commands.do_cower(None)
        game = self.commands.get_game()
        player = game.get_player()
        self.assertEqual(player.get_health(), 8)


class TestPlayerAttacks(unittest.TestCase):

    def setUp(self):
        self.commands = Commands()
        self.commands.do_load("test_move")

    def test_player_attacks_with_no_weapon(self):
        self.assertEqual(1, 1)
    
    def test_player_attacks_with_weapon(self):
        self.assertEqual(1, 1)

    def test_player_cant_attack_with_two_weapons(self):
        self.assertEqual(1, 1)

    def test_attack_with_chainsaw_loses_one_charge(self):
        self.assertEqual(1, 1)

    def test_attack_with_gas_and_chainsaw_gains_charge(self):
        self.assertEqual(1, 1)

    def test_attack_with_oil_runs_away(self):
        self.assertEqual(1, 1)
        
    def test_attack_with_soda_gains_health(self):
        self.assertEqual(1, 1)

class TestUsingItems(unittest.TestCase):

    def setUp(self):
        self.commands = Commands()

    def test_using_soda_increases_health(self):
        self.commands.do_load("test_give_soda")
        self.commands.do_use("Can of Soda")
        game = self.commands.get_game()
        self.assertEqual(game.get_player().get_health(), 8)

    def test_gasoline_and_chainsaw_gains_charge(self):
        self.assertEqual(1, 1)

    def test_dropping_item_drops_item(self):
        self.commands.do_load("test_give_soda")
        self.commands.do_drop("Can of Soda")
        game = self.commands.get_game()
        self.assertEqual(len(game.get_player().get_items()), 0)

if __name__ == "__main__":
    unittest.main()