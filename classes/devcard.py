class DevCard:
    """
    >>> from classes.devcard import DevCard
    >>> devcard = DevCard("Machete", "Unlimited", "Zombies", "Health", "Item")
    >>> devcard.get_item()
    'Machete'
    >>> devcard.get_charges()
    'Unlimited'
    >>> devcard.get_event_at_time(9)
    'Zombies'
    >>> devcard.get_event_at_time(10)
    'Health'
    >>> devcard.get_event_at_time(11)
    'Item'
    >>> devcard_two = DevCard("Can Of Soda", "1", "Health", "Health", "Item")
    >>> devcard_two.get_event_at_time(11)
    'Item'
    >>> devcard_two.get_event_at_time(10)
    'Health'
    >>> devcard_two.get_item()
    'Can Of Soda'
    >>> devcard_two.get_charges()
    1

    """
    def __init__(self, item, charges, event_one, event_two, event_three):
        self.item = item
        self.charges = charges
        self.event_one = event_one
        self.event_two = event_two
        self.event_three = event_three

        if self.charges != "Unlimited":
            self.charges = int(self.charges)

    def get_event_at_time(self, time):
        if time == 9:
            return self.event_one
        elif time == 10:
            return self.event_two
        elif time == 11:
            return self.event_three

    def get_item(self):
        return self.item

    def get_charges(self):
        return self.charges
