import random
import numpy as np
import itertools

NUM_PLAYERS = 4
NUM_HS = 9
NUM_CARDS_PER_HS = 6
TOTAL_CARDS = NUM_HS * NUM_CARDS_PER_HS
GAME_INFO = (NUM_HS, NUM_CARDS_PER_HS, NUM_PLAYERS)

"""
class Fish:
    def __init__(self, game):
"""


class Player:
    def __init__(self, name, game_info=GAME_INFO):
        self.name = name
        self.information = np.zeros(game_info)

        self.own = self.information[:, :, 0]
        self.partner = self.information[:, :, 1]
        self.opponent1 = self.information[:, :, 2]
        self.opponent2 = self.information[:, :, 3]

        self.num_players = GAME_INFO[-1]
        self.num_hs = GAME_INFO[0]

    def initialize_information(self, hand):
        for hs, card in hand:
            self.own[hs, card] = 1
            for other in range(1, self.num_players):
                self.information[hs, card, other] = -1
        self.own[np.where(self.own != 1)] = -1

    def update_information(self, interrogator, suspect):
        pass

    def get_hand(self):
        return [tuple(card) for card in np.argwhere(self.own == 1)]

    def has_card(self, card):
        return bool(self.own[card])

    def get_valid_asks(self):
        self.own[np.where(np.sum(self.own, axis=1) == -self.num_hs)] = 0
        return [tuple(card) for card in np.argwhere(self.own == -1)]


def deal_cards(num_hs, num_cards_per_hs, players):
    # initialize the cards and shuffle them
    cards = list(itertools.product([hs for hs in range(num_hs)], [card for card in range(num_cards_per_hs)]))
    random.shuffle(cards)

    # determine the number of players and the number of cards each player should receive, then distribute
    num_players = len(players)
    cards_per_player = num_hs * num_cards_per_hs / num_players
    for i in range(num_players):
        players[i].initialize_information(cards[int(i * cards_per_player): int((i + 1) * cards_per_player)])


if __name__ == '__main__':
    random.seed(0)
    edgar, alina, lucas, william = Player("edgar"), Player("alina"), Player("lucas"), Player("william")
    gamers = [edgar, alina, lucas, william]
    deal_cards(NUM_HS, NUM_CARDS_PER_HS, gamers)

    print(william.own)
    print(william.get_hand())
    print(william.get_valid_asks())




