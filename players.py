import random
import numpy as np

class Player:
    def __init__(self, name):
        self.name = name
        self.index = None
        self.hand = []
        self.team = name
        self.deck = None
        # computer only values
        self.information = None
        self.ask_queue = []
        self.declare_queue = []

    def sort_hand(self):
        self.hand.sort()

    def display_hand(self):
        print(self.name, "has ", end='')
        self.sort_hand()
        hand_size = len(self.hand)
        if hand_size > 0:
            for i in range(hand_size - 1):
                card = self.hand[i]
                card.display()
                print(end=", ")
            card = self.hand[hand_size - 1]
            card.display()
        print()

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
            if self.hand[i].suit != self.hand[i+cards_per_suit-1].suit:
                return False
        return True

    """
        returns a valid card + opponent to ask (generated at random)
    """

    def get_next(self, game):  # random
        # TODO: implement declaring on other's (notably teammates') turns
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
        # if you run out of cards, pick a teammate to start
        if len(self.hand) == 0:
            # TODO: generate a valid person to switch to (currently random) - probably make this a method
            for player in self.team.players:
                if len(player.hand) != 0:
                    print(self.name, "passes power to", player.name)
                    return None, player
            return None, None
        else:
            # TODO: make this cleaner - maybe make a separate method
            # generate a player from the opposing team
            opponent = game.players[random.randint(0, len(game.players) - 1)]
            while self.team == opponent.team or len(opponent.hand) == 0:  # can also enforce len(opponent.hand) != 0
                opponent = game.players[random.randint(0, len(game.players) - 1)]
            # generate a valid card to ask
            card = game.deck.cards[random.randint(0, len(game.deck.cards) - 1)]
            while not self.is_valid_ask(card):
                card = game.deck.cards[random.randint(0, len(game.deck.cards) - 1)]
            # don't ask for cards you know the opponent doesn't have
            asked_before = (self.information.card_distribution[card.suit - 1, self.deck.values.index(card.value), game.players.index(opponent)] == -1)
            while asked_before:
                # generate a player from the opposing team
                opponent = game.players[random.randint(0, len(game.players) - 1)]
                while self.team == opponent.team or len(opponent.hand) == 0:  # can also enforce len(opponent.hand) != 0
                    opponent = game.players[random.randint(0, len(game.players) - 1)]
                # generate a valid card to ask
                card = game.deck.cards[random.randint(0, len(game.deck.cards) - 1)]
                while not self.is_valid_ask(card):
                    card = game.deck.cards[random.randint(0, len(game.deck.cards) - 1)]
                asked_before = (self.information.card_distribution[card.suit - 1, self.deck.values.index(card.value), game.players.index(opponent)] == -1)
        return card, opponent
