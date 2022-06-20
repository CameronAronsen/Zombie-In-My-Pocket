import unittest
from main import Commands


class TestDifficulty(unittest.TestCase):
    def setUp(self):
        self.commands = Commands()

    def test_difficulty_easy(self):
        self.commands.do_start(None)
        self.commands.do_difficulty("Easy")
        self.assertEqual(self.commands.get_game().difficulty, "Easy")

    def test_easy_sets_player_health(self):
        self.commands.do_start(None)
        self.commands.do_difficulty("Easy")
        self.assertEqual(self.commands.get_game().get_player().get_health(),
                         10)

    def test_easy_sets_player_attack(self):
        self.commands.do_start(None)
        self.commands.do_difficulty("Easy")
        self.assertEqual(self.commands.get_game().get_player().get_attack(),
                         2)

    def test_difficulty_medium(self):
        self.commands.do_start(None)
        self.commands.do_difficulty("Medium")
        self.assertEqual(self.commands.get_game().difficulty, "Medium")

    def test_medium_sets_player_health(self):
        self.commands.do_start(None)
        self.commands.do_difficulty("Medium")
        self.assertEqual(self.commands.get_game().get_player().get_health(),
                         6)

    def test_medium_sets_player_attack(self):
        self.commands.do_start(None)
        self.commands.do_difficulty("Medium")
        self.assertEqual(self.commands.get_game().get_player().get_attack(),
                         1)

    def test_difficulty_hard(self):
        self.commands.do_start(None)
        self.commands.do_difficulty("Hard")
        self.assertEqual(self.commands.get_game().difficulty, "Hard")

    def test_hard_sets_player_health(self):
        self.commands.do_start(None)
        self.commands.do_difficulty("Hard")
        self.assertEqual(self.commands.get_game().get_player().get_health(),
                         4)

    def test_hard_sets_player_attack(self):
        self.commands.do_start(None)
        self.commands.do_difficulty("Hard")
        self.assertEqual(self.commands.get_game().get_player().get_attack(),
                         1)

    def test_difficulty_invalid(self):
        self.commands.do_difficulty("Invalid")
        self.assertEqual(self.commands.get_game().state, "Starting")

if __name__ == "__main__":
    unittest.main()
