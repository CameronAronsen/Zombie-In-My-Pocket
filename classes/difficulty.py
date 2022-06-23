from classes.abstract_difficulty import AbstractDifficulty

class EasyDifficulty(AbstractDifficulty):
    def __init__(self, game):
        self.game = game

    def set_difficulty(self):
        self.game.difficulty = "Easy"
        player = self.game.get_player()
        player.set_health(10)
        player.set_attack(2)

class MediumDifficulty(AbstractDifficulty):
    def __init__(self, game):
        self.game = game

    def set_difficulty(self):
        self.game.difficulty = "Medium"
        player = self.game.get_player()
        player.set_health(6)
        player.set_attack(1)

class HardDifficulty(AbstractDifficulty):
    def __init__(self, game):
        self.game = game

    def set_difficulty(self):
        self.game.difficulty = "Hard"
        player = self.game.get_player()
        player.set_health(4)
        player.set_attack(1)
