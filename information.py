import numpy as np


class Information:
    def __init__(self, deck, players, player):
        # self.players = players
        self.player_index = players.index(player)
        # 0 indicates unknown, 1 indicates has the card, -1 indicates doesn't have the card
        self.card_distribution = np.zeros((deck.no_of_suits, deck.cards_per_suit, len(players)))
        # card status: indicates whether a card's location is known
        self.card_status = np.zeros((deck.no_of_suits, deck.cards_per_suit))
        # player status: indicates whether a player has unknown cards in a half-suit
        self.player_status = np.zeros((deck.no_of_suits, len(players)))
        # initialize based on player's hand
        for card in deck.cards:
            if card in player.hand:
                self.card_status[card.suit_index, card.value_index] = 1
                self.card_distribution[card.suit_index, card.value_index, :] = -1
                self.card_distribution[card.suit_index, card.value_index, player.index] = 1
            else:
                self.card_distribution[card.suit_index, card.value_index, player.index] = -1





    def extrapolate(self, suit_index):
        # additional extrapolation (over the suit)
        cards_per_suit = self.card_distribution.shape[1]
        no_of_players = self.card_distribution.shape[2]
        for value_index in range(cards_per_suit):
            # One person is unknown, everybody else doesn't have card
            if np.sum(self.card_distribution[suit_index, value_index, :]) == 1 - no_of_players:
                owner_index = np.where(self.card_distribution[suit_index][value_index, :] == 0)[0][0]
                # before changing, check if player status is 1 and if it is 1, change then to 0 then make the deduction
                if self.player_status[suit_index, owner_index] == 1:
                    self.player_status[suit_index, owner_index] = 0
                self.card_distribution[suit_index, value_index, owner_index] = 1
                self.card_status[suit_index, value_index] = 1
        for player_index in range(no_of_players):
            # Player has an unknown card, only one option for unknown
            if self.player_status[suit_index, player_index] == 1 and player_index != self.player_index:
                unknown_index_array = np.where(self.card_distribution[suit_index][:, player_index] == 0)[0]
                if len(unknown_index_array) == 1:
                    # Suits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    # Values = ['\u2654', '\u2655', '\u2656', '\u2657', '\u2658', '\u2659']
                    # print(self.player_index, "can extrapolate", player_index, "has", Values[unknown_index_array[0]], "of", Suits[card.suit_index])
                    # value_index = unknown_index_array[0]
                    self.card_status[suit_index, unknown_index_array[0]] = 1
                    self.card_distribution[suit_index, unknown_index_array[0], :] = -1
                    self.card_distribution[suit_index, unknown_index_array[0], player_index] = 1
                    self.player_status[suit_index, player_index] = 0

    """
    Checks if a player can clear some suit (has full knowledge over some suit: always safe to ask)
    """
    def check_for_clear(self, game, current_player):
        added_to_queue = False
        # iterate over all remaining suits
        for suit in game.deck.suits:
            # TODO: Find a better way to represent suit index instead of hard-coding it
            suit_index = suit - 1
            # check if the player has the suit & full knowledge of the suit
            if current_player.has_suit(suit) and np.sum(self.card_status[suit_index]) == game.deck.cards_per_suit:
                # for each card in the suit, add to ask_queue if an opponent is holding the card
                for value_index in range(game.deck.cards_per_suit):
                    owner_index = np.where(self.card_distribution[suit_index][value_index, :] == 1)[0]
                    #print("owner_index", owner_index, "owns", game.deck.values[value_index], "of", suit)
                    if len(owner_index) == 0:
                        print(current_player.name, self.card_distribution[suit_index], self.card_status[suit_index], "time to crash :(")
                    owner = game.players[owner_index[0]]
                    if current_player.team != owner.team:
                        card = sorted(game.deck.cards)[suit_index * game.deck.cards_per_suit + value_index]
                        current_player.ask_queue.append((card, owner))
                        added_to_queue = True
                        #printing
                        print(current_player.name, "knows", owner.name, "has the ", end='')
                        card.display()
                        print("!")
        return added_to_queue

    """
        Checks if a player can declare some suit 
        Returns list of suits that can be declared
    """

    def check_for_declare(self, game, current_player):
        declarable = []
        # iterate over all remaining suits
        for suit in game.deck.suits:
            can_declare_suit = False
            # TODO: Find a better way to represent suit index instead of hard-coding it
            suit_index = suit - 1
            # check if the player has the suit & full knowledge of the suit
            if current_player.has_suit(suit) and np.sum(self.card_status[suit_index]) == game.deck.cards_per_suit:
                can_declare_suit = True
                # for each card in the suit, add to ask_queue if an opponent is holding the card
                for value_index in range(game.deck.cards_per_suit):
                    owner_index = np.where(self.card_distribution[suit_index][value_index, :] == 1)[0]
                    # print("owner_index", owner_index, "owns", game.deck.values[value_index], "of", suit)
                    if len(owner_index) == 0:
                        print(current_player.name, self.card_distribution[suit_index], self.card_status[suit_index], "time to crash :(")
                    owner = game.players[owner_index[0]]
                    # cannot declare the suit if someone on opposite team has card
                    if current_player.team != owner.team:
                        can_declare_suit = False
            # add the suit to declareable
            if can_declare_suit:
                declarable.append(suit)
        return declarable
