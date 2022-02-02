import random
import numpy as np
import itertools
from game import Fish

NUM_PLAYERS = 4
NUM_HS = 9
NUM_CARDS_PER_HS = 6
TOTAL_CARDS = NUM_HS * NUM_CARDS_PER_HS
GAME_INFO = (NUM_HS, NUM_CARDS_PER_HS + 1, NUM_PLAYERS)


class Player:
    def __init__(self, name, game_info=GAME_INFO):
        self.name = name
        self.information = np.zeros(game_info)
        self.num_hs = GAME_INFO[0]
        self.num_cards_per_hs = GAME_INFO[1] - 1
        self.num_players = GAME_INFO[2]
        #self.team = name
        self.player_to_information = {}
        ###
        # computer only values
        #self.information = None
        self.ask_queue = []
        self.declare_queue = []

    def initialize_p2i(self, team_mine, team_opponent):
        self.player_to_information[self.name] = self.information[:, :, 0]
        index = 1
        for player in team_mine:
            if self != player:
                self.player_to_information[player.name] = self.information[:, :, index]
                index += 1
        for player in team_opponent:
            self.player_to_information[player.name] = self.information[:, :, index]
            index += 1

    def initialize_information(self, hand):
        for hs, value in hand:
            self.player_to_information[self.name][hs, value] = 1
            for other in range(1, self.num_players):
                self.information[hs, value, other] = -1
        self.player_to_information[self.name][np.where(self.player_to_information[self.name] != 1)] = -1

    def get_hand(self):
        return [tuple(card) for card in np.argwhere(self.player_to_information[self.name] == 1)]

    def has_card(self, card):
        return bool(self.player_to_information[self.name][card])

    def get_valid_asks(self):
        # TODO: change this so that we don't add the last entry (which corresponds to 0/1 about if extra half suit)
        self.player_to_information[self.name][np.where(np.sum(self.player_to_information[self.name], axis=1) == -self.num_hs)] = 0
        return [tuple(card) for card in np.argwhere(self.player_to_information[self.name] == -1)]

    """
        Updates information after someone out of cards
    """
    def update_out_of_cards(self, player):
        self.player_to_information[player.name] = -1
        #self.extrapolate()

    """
        Updates information after someone asks for a card
    """
    def update(self, current_player, card, opponent, got_card):
        # if we didn't know the player had a card in the suit, update player status to 1 for that suit
        if 1 not in self.player_to_information[current_player.name][card[0], :-1]:
            self.player_to_information[current_player.name][card[0], -1] = 1
        if got_card:
            # if we knew the player had a card in the suit, which card could have been the one taken,
            # update player status to 0 for that suit
            if self.player_to_information[opponent.name][card] == 0:
                self.player_to_information[opponent.name][card[0], -1] = 0

            # distribution: indicate we know where the card is and who has it
            self.information[card, :] = -1
            self.player_to_information[current_player.name][card] = 1
        else:
            # distribution: indicate neither player has the card
            self.player_to_information[current_player.name][card] = -1
            self.player_to_information[opponent.name][card] = -1
        # self.extrapolate()



    def extrapolate(self):
        for hs in range(self.num_hs):
            for value in range(self.num_cards_per_hs):
                # One person is unknown, everybody else doesn't have car
                if np.sum(self.information[hs, value, :]) == 1 - self.num_players:
                    owner_index = np.where(self.information[hs][value, :] == 0)[0][0]
                    # before changing, check if player status is 1 and if it is 1, change then to 0 then make the deduction
                    if self.player_status[hs, owner_index] == 1:
                        self.player_status[hs, owner_index] = 0
                    self.information[hs, value, owner_index] = 1
            for player_index in range(self.num_players):
                # Player has an unknown card, only one option for unknown
                if self.player_status[hs, player_index] == 1 and player_index != self.player_index:
                    unknown_index_array = np.where(self.information[hs][:, player_index] == 0)[0]
                    if len(unknown_index_array) == 1:
                        self.information[hs, unknown_index_array[0], :] = -1
                        self.information[hs, unknown_index_array[0], player_index] = 1
                        self.player_status[hs, player_index] = 0

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

if __name__ == '__main__':
    random.seed(0)
    edgar, alina, lucas, william = Player("edgar"), Player("alina"), Player("lucas"), Player("william")
    gamers = [edgar, alina, lucas, william]
    # deal_cards(NUM_HS, NUM_CARDS_PER_HS, gamers)
    game = Fish(gamers)
    print(william.player_to_information[william.name])
    print(edgar.player_to_information[william.name])
    print(edgar.get_hand())
    print(edgar.get_valid_asks())