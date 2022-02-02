import random
import numpy as np


class Player:
    def __init__(self, name):
        self.name = name
        # game constants
        self.num_hs = 9
        self.num_cards_per_hs = 6
        self.can_ask_for_own_card = False
        self.hand_size_public = False
        # can ask for own card? display public hand size?
        # teammates and opponents (needs to be private)
        self.teammates = []
        self.opponents = []
        # hand
        self.hand = -np.ones((self.num_hs, self.num_cards_per_hs))
        self.num_cards = 0

        #self.index = None
        # computer only values
        self.information = None
        self.ask_queue = []
        self.declare_queue = []

    def initialize_hand(self, hand):
        for hs, value in hand:
            self.hand[hs, value] = 1
        self.num_cards = (self.hand == 1).sum()

    # unused
    def get_hand(self):
        return [tuple(card) for card in np.argwhere(self.hand == 1).tolist()]

    def get_next(self):
        if self.num_cards == 0:
            selected_teammate = None
            invalid_teammate = True
            print("out of cards, pick teammate")
            return None, selected_teammate
        else:
            selected_card = None
            selected_opponent = None
            invalid_card = True
            invalid_opponent = True
            print(self.name, self.get_hand())
            print(self.get_valid_asks())
            while invalid_card:
                selected_card = eval(input("Pick card: \n"))
                if selected_card in self.get_valid_asks():
                    invalid_card = False
            opponent_names = [opponent.name for opponent in self.opponents]
            while invalid_opponent:
                print(opponent_names)
                selected_opponent = input("Pick opponent: \n")
                if selected_opponent in opponent_names:
                    invalid_opponent = False
            selected_opponent = self.opponents[opponent_names.index(selected_opponent)]
            return selected_card, selected_opponent

    # called in game.py
    def has_card(self, card):
        return self.hand[card] == 1

    # change this to incorporate if can ask for own card (i.e. has card in half suit)
    def get_valid_asks(self):
        self.hand[np.where(np.sum(self.hand, axis=1) == -self.num_hs)] = 0
        return [tuple(card) for card in np.argwhere(self.hand == -1)]

    def update(self, current_player, card, next_player, got_card):
        if got_card == True:
            if self == current_player:
                self.add_card(card)
            if self == next_player:
                self.remove_card(card)

    def add_card(self, card):
        self.hand[card] = 1
        self.num_cards += 1

    def remove_card(self, card):
        self.hand[card] = -1
        self.num_cards -= 1

    # unused (declare separate button)
    def get_declarable_suits(self):
        cards = self.get_hand()
        suits = set()
        for suit, value in cards:
            suits.add(suit)
        return sorted(list(suits))







class Computer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.information = None
        self.ask_queue = []
        self.declare_queue = []

        # TODO: make has_suit & has_card more efficient by implementing binary search
        def has_suit(self, suit_to_check):
            for card in self.hand:
                if card.suit == suit_to_check:
                    return True
            return False

        def has_card(self, card_to_check):
            for card in self.hand:
                if card == card_to_check:
                    return True
            return False

        """ 
        Given a card, returns a boolean indicating whether the player can legally ask for that card.
        """

        def is_valid_ask(self, card, can_be_own_card=False):
            # cannot ask anyone for a card if you don't have a card of the same suit
            if not self.has_suit(card.suit):
                return False
            # cannot ask for a card you have (if setting is disabled)
            if not can_be_own_card and self.has_card(card):
                return False
            return True

    """ 
        Returns a boolean indicating whether a player cannot legally ask for any card
        Note: this method is currently not being used, but might be useful for implementing human players
        """

    def no_asks_left(self, cards_per_suit):
        # cannot ask if hand has no cards
        if len(self.hand) == 0:
            return True
        self.hand.sort()
        # if hand is not all full suits, can ask for some card
        if len(self.hand) % cards_per_suit != 0:
            return False
        # since sorted, check if each consecutive group is a full suit
        for i in range(0, len(self.hand), cards_per_suit):
            if self.hand[i].suit != self.hand[i + cards_per_suit - 1].suit:
                return False
        return True

    """
        returns a valid card + opponent to ask (generated at random)
    """
    def get_next(self):  # random
        # TODO: implement declaring on other's (notably teammates') turns
        """
        declarable = self.information.check_for_declare(game, self)
        print(self.name, "can declare", declarable)
        while len(declarable) > 0:
            suit_to_declare = declarable.pop()
            self.team.declare(self, game, suit_to_declare)
        # we do this first to skip game.information.check if possible
        while len(self.ask_queue) > 0:
            next_ask = self.ask_queue.pop()
            return next_ask[0], next_ask[1]
        if self.information.check_for_clear(game, self):
            # we added asks to the queue
            next_ask = self.ask_queue.pop()
            return next_ask[0], next_ask[1]
        """

        # if you run out of cards, pick a teammate to start
        if len(self.get_hand()) == 0:
            for player in self.teammates:
                if len(player.get_hand()) != 0:
                    print(self.name, "passes power to", player.name)
                    return None, player
            return None, None
        else:
            # randomly select a card and an opponent
            valid_asks = self.get_valid_asks()
            selected_card = valid_asks[random.randint(0, len(valid_asks) - 1)]
            selected_opponent = self.opponents[random.randint(0, len(self.opponents) - 1)]
            return selected_card, selected_opponent
