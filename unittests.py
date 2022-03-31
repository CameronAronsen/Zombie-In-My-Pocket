import unittest
from os.path import exists
from main import Commands
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
        self.assertEqual(player_pos, (15, 15))

    def test_save_saves_current_game(self):
        self.commands.do_start(None)
        self.commands.do_place(None)
        self.commands.do_save("test_saving")
        self.assertTrue(exists("./saves/test_saving.db.dat"))
        pass

    def test_restart_restarts_game(self):
        self.commands.do_start(None)
        self.commands.do_load("test_bury_totem")
        self.commands.do_restart(None)
        self.commands.do_start(None)
        self.commands.do_place(None)
        game = self.commands.get_game()
        current_tile = game.get_current_tile()
        self.assertEqual(current_tile.get_name(), "Foyer")


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
        self.assertEqual(player_pos, (15, 14))

    def test_player_moves_south(self):
        self.commands.do_s(None)
        self.commands.do_rotate(None)
        self.commands.do_rotate(None)
        self.commands.do_place(None)
        game = self.commands.get_game()
        player_pos = game.get_player_x(), game.get_player_y()
        self.assertEqual(player_pos, (15, 16))

    def test_player_moves_east(self):
        self.commands.do_e(None)
        self.commands.do_place(None)
        game = self.commands.get_game()
        player_pos = game.get_player_x(), game.get_player_y()
        self.assertEqual(player_pos, (15, 15))

    def test_player_moves_west(self):
        self.commands.do_w(None)
        self.commands.do_rotate(None)
        self.commands.do_place(None)
        game = self.commands.get_game()
        player_pos = game.get_player_x(), game.get_player_y()
        self.assertEqual(player_pos, (14, 15))

    def test_north_from_dining_room_goes_to_patio(self):
        self.commands.do_n(None)
        self.commands.do_rotate(None)
        self.commands.do_rotate(None)
        self.commands.do_place(None)
        game = self.commands.get_game()
        current_tile = game.get_current_tile()
        self.assertEqual(current_tile.get_name(), "Patio")

    def test_zombies_break_through_wall(self):
        self.commands.do_load("test_zombie_break_wall")
        self.commands.do_choose("n")
        game = self.commands.get_game()
        self.assertEqual(game.state, "Attacking")

    def test_cower_gains_health(self):
        self.commands.do_cower(None)
        game = self.commands.get_game()
        player = game.get_player()
        self.assertEqual(player.get_health(), 7)


class TestPlayerAttacks(unittest.TestCase):
    def setUp(self):
        self.commands = Commands()

    def test_player_attacks_with_no_weapon(self):
        self.commands.do_load("test_chainsaw_gasoline")
        self.commands.do_attack("")
        game = self.commands.get_game()
        player = game.get_player()
        self.assertEqual(player.get_health(), 3)

    def test_player_attacks_with_weapon(self):
        self.commands.do_load("test_chainsaw_gasoline")
        self.commands.do_attack("Chainsaw")
        game = self.commands.get_game()
        player = game.get_player()
        self.assertEqual(player.get_health(), 6)

    def test_player_cant_attack_with_two_weapons(self):
        self.commands.do_load("test_two_weapons")
        self.commands.do_attack("Machete, Golf Club")
        game = self.commands.get_game()
        self.assertEqual(game.state, "Attacking")

    def test_attack_with_chainsaw_loses_one_charge(self):
        self.commands.do_load("test_chainsaw_gasoline")
        self.commands.do_attack("Chainsaw")
        game = self.commands.get_game()
        self.assertEqual(game.get_player().get_items()[0][1], 1)

    def test_attack_with_gas_and_chainsaw_gains_charge(self):
        self.commands.do_load("test_chainsaw_gasoline")
        self.commands.do_attack("Chainsaw, Gasoline")
        game = self.commands.get_game()
        self.assertEqual(game.get_player().get_items()[0][1], 3)

    def test_attack_with_soda_gains_health(self):
        self.commands.do_load("test_can_of_soda")
        self.commands.do_attack("Can of Soda")
        game = self.commands.get_game()
        player = game.get_player()
        self.assertEqual(player.get_health(), 7)

    def test_attack_with_candle_gasoline_kills_zombies(self):
        self.commands.do_load("test_gasoline_candle")
        self.commands.do_attack("gasoline, candle")
        game = self.commands.get_game()
        player = game.get_player()
        self.assertEqual(player.get_health(), 7)

    def test_attack_with_candle_oil_kills_zombies(self):
        self.commands.do_load("test_oil_candle")
        self.commands.do_attack("oil, candle")
        game = self.commands.get_game()
        player = game.get_player()
        self.assertEqual(player.get_health(), 6)

    def test_cant_use_invalid_item(self):
        self.commands.do_load("test_oil_candle")
        self.commands.do_attack("machete")
        game = self.commands.get_game()
        self.assertEqual(game.state, "Attacking")

    def test_attack_with_oil_runs_away(self):
        self.commands.do_load("test_oil_flee")
        self.commands.do_attack("oil")
        game = self.commands.get_game()
        current_tile = game.get_current_tile()
        self.assertEqual(current_tile.get_name(), "Foyer")

    def test_cant_attack_with_item_not_in_inventory(self):
        self.commands.do_load("test_oil_candle")
        self.commands.do_attack("machete")
        game = self.commands.get_game()
        self.assertEqual(game.state, "Attacking")

    def test_run_away(self):
        self.commands.do_load("test_oil_candle")
        self.commands.do_run("e")
        game = self.commands.get_game()
        player = game.get_player()
        self.assertEqual(player.get_health(), 5)


class TestUsingItems(unittest.TestCase):
    def setUp(self):
        self.commands = Commands()

    def test_using_soda_increases_health(self):
        self.commands.do_load("test_give_soda")
        self.commands.do_use("Can of Soda")
        game = self.commands.get_game()
        self.assertEqual(game.get_player().get_health(), 8)

    def test_gasoline_and_chainsaw_gains_charge(self):
        self.commands.do_load("test_use_chainsaw_gasoline")
        self.commands.do_use("Chainsaw, Gasoline")
        game = self.commands.get_game()
        self.assertEqual(game.get_player().get_items()[0][1], 4)

    def test_dropping_item_drops_item(self):
        self.commands.do_load("test_give_soda")
        self.commands.do_drop("Can of Soda")
        game = self.commands.get_game()
        self.assertEqual(len(game.get_player().get_items()), 0)

    def test_cant_use_invalid_item(self):
        self.commands.do_load("test_use_chainsaw_gasoline")
        self.commands.do_use("Chainsaw")
        game = self.commands.get_game()
        self.assertEqual(game.get_player().get_items()[0][1], 2)

    def test_cant_use_item_not_in_inventory(self):
        self.commands.do_load("test_totem_pickup")
        self.commands.do_use("Chainsaw, Gasoline")
        game = self.commands.get_game()
        self.assertEqual(game.get_player().get_items()[0], ["Gasoline", 1])

    def test_pick_up_totem(self):
        self.commands.do_load("test_totem_pickup")
        self.commands.do_search("testing")
        game = self.commands.get_game()
        self.assertTrue(game.get_player().get_totem())

    def test_bury_totem_wins_game(self):
        self.commands.do_load("test_bury_totem")
        self.commands.do_bury("testing")
        game = self.commands.get_game()
        self.assertEqual(game.state, "Game Over")


if __name__ == "__main__":
    unittest.main()
