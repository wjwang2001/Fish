import random
import numpy as np
from information import Information


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

    def initialize_hand(self, hand):
        for hs, value in hand:
            self.hand[hs, value] = 1
        self.num_cards = (self.hand == 1).sum()

    # unused except for in print debugging and user card prompting
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
        self.players = [self] #teammates and opponents added in initialize_hand
        self.information = None
        self.ask_queue = []
        self.declare_queue = []

    def initialize_hand(self, hand):
        # same as human player initialize function
        for hs, value in hand:
            self.hand[hs, value] = 1
        self.num_cards = (self.hand == 1).sum()
        # now that hand is dealt, initialize information
        self.players.extend(self.teammates)
        self.players.extend(self.opponents)
        self.information = Information(self.num_hs, self.num_cards_per_hs, self.players)

    def update(self, current_player, card, next_player, got_card):
        # same as human player update function
        if got_card:
            if self == current_player:
                self.add_card(card)
            if self == next_player:
                self.remove_card(card)
        # computer update TODO: account in logic for if current player or next_player is same as self.player
        hs = card[0]
        value = card[1]
        current_player_index = self.information.players.index(current_player)
        askee_index = self.information.players.index(next_player)
        # if we didn't know the player had a card in the suit, update player status to 1 for that suit
        #if 1 not in self.information.player_status[card[0], current_player_index]:
        self.information.player_status[card[0], current_player_index] = 1
        if got_card:
            # if we knew the player had a card in the suit, which card could have been the one taken,
            # update player status to 0 for that suit
            #if self.information[opponent.name][card] == 0:
            self.information.player_status[hs, askee_index] = 0

            # distribution: indicate we know where the card is and who has it
            self.information.card_distribution[hs, value, :] = -1
            self.information.card_distribution[hs, value, current_player_index] = 1
        else:
            # distribution: indicate neither player has the card
            self.information.card_distribution[hs, value, current_player_index] = -1
            self.information.card_distribution[hs, value, askee_index] = -1
        self.information.extrapolate(card)

    """
        returns a valid card + opponent to ask (generated at random)
        working on implementing logical deductions
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
        """
        #information
        #"""
        while len(self.ask_queue) > 0:
            next_ask = self.ask_queue.pop()
            return next_ask[0], next_ask[1]
        if self.information.check_for_clear():
            # we added asks to the queue
            next_ask = self.ask_queue.pop()
            return next_ask[0], next_ask[1]
        #"""

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
