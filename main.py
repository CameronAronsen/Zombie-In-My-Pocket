class Game:
    def __init__(self, player, time=9):
        self.player = player
        self.time = time

    def draw_card(self):
        pass

    def get_game(self):
        return print(f'The player has {self.player.get_health()} health and {self.player.get_attack()} attack the '
                     f'time is {self.time}')


class Player:
    def __init__(self, attack=1, health=6):
        self.attack = attack
        self.health = health

    def get_health(self):
        return self.health

    def get_attack(self):
        return self.attack

    def set_attack(self, attack):
        self.attack = attack

    def set_health(self, health):
        self.health = health


class DevCards:
    def __init__(self):
        pass


class Tile:
    def __init__(self):
        pass


def main():
    player = Player()
    game = Game(player)
    game.get_game()
    game.get_game()

if __name__ == "__main__":
    main()
