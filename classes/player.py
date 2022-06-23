class Player:
    """
    >>> from classes.player import Player
    >>> player = Player()
    >>> player.get_health()
    6
    >>> player.get_attack()
    1
    >>> player.get_items()
    []
    >>> player.add_item("Machete", 1)
    >>> player.get_items()
    [['Machete', 1]]
    >>> player.get_item_charges("Machete")
    1
    >>> player.get_move_count()
    0
    >>> player.increment_move_count()
    >>> player.increment_move_count()
    >>> player.get_move_count()
    2

    """

    def __init__(self, attack=1, health=6, x=16, y=16, has_totem=False):
        self.attack = attack
        self.health = health
        self.x = x
        self.y = y
        self.items = []
        self.has_totem = has_totem
        self.move_count = 0
        self.difficulty = None

    def get_health(self):
        return self.health

    def found_totem(self):
        self.has_totem = True

    def get_attack(self):
        return self.attack

    def set_attack(self, attack):
        self.attack = attack

    def set_health(self, health):
        self.health = health

    def add_health(self, health):
        self.health += health

    def add_attack(self, attack):
        self.attack += attack

    def get_items(self):
        return self.items

    def get_totem(self):
        return self.has_totem

    def get_item_charges(self, item):
        for check_item in self.get_items():
            if check_item[0] == item:
                return check_item[1]

    def set_item_charges(self, item, charge):
        for check_item in self.get_items():
            if check_item[0] == item:
                check_item[1] = charge

    def use_item_charge(self, item):
        for check_item in self.get_items():
            if check_item[0] == item:
                check_item[1] -= 1

    def add_item(self, item, charges):
        if len(self.items) < 2:
            self.items.append([item, charges])

    def remove_item(self, item):
        self.items.pop(self.items.index(item))

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_move_count(self):
        return self.move_count

    def set_move_count(self, count):
        self.move_count = count

    def increment_move_count(self):
        self.move_count += 1

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def trigger_difficulty(self):
        self.difficulty.set_difficulty()
