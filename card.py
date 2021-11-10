class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.suit_index = None
        self.value_index = None

    # sorting by suit
    def __lt__(self, other):
        if self.suit < other.suit:
            return True
        elif self.suit == other.suit and self.value < other.value:
            return True
        return False

    def __eq__(self, other):
        if self.suit == other.suit and self.value == other.value:
            return True
        return False

    def display(self):
        print(self.value, "of", self.suit, end='')



"""
from enum import Enum

class Values(Enum):
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13
    ace = 14
    two = 15

    def __repr__(self):
        if self.value <= 10:
            return str(self.value)
        else:
            return ['J', 'Q', 'K', 'A', '2'][self.value - 11]

    def __lt__(self, other):
        return self.value < other.value
"""