import numpy as np


class Information:
    def __init__(self, num_hs, num_cards_per_hs, players):
        self.num_hs = num_hs
        self.num_cards_per_hs = num_cards_per_hs
        self.players = players
        # when 2n players, player 0 is player, players 1 to n-1 are teammates, players n to 2n-1 are opponents
        self.player_index = 0
        self.player = players[self.player_index]
        # 0 indicates unknown, 1 indicates has the card, -1 indicates doesn't have the card
        self.card_distribution = np.zeros((num_hs, num_cards_per_hs, len(players)))
        # card status: indicates whether a card's location is known
        #self.card_status = np.zeros((num_hs, num_cards_per_hs))
        # player status: indicates whether a player has unknown cards in a half-suit
        self.player_status = np.zeros((num_hs, len(players)))
        # initialize based on player's hand
        for half_suit in range(num_hs):
            for value in range(num_cards_per_hs):
                card = (half_suit, value)
                if card in self.player.get_hand():
                    #self.card_status[card.suit_index, card.value_index] = 1
                    self.card_distribution[half_suit, value, :] = -1
                    self.card_distribution[half_suit, value, self.player_index] = 1
                else:
                    self.card_distribution[half_suit, value, self.player_index] = -1

    def extrapolate(self, card):
        hs = card[0]
        # additional extrapolation (over the suit)
        cards_per_suit = self.card_distribution.shape[1]
        no_of_players = self.card_distribution.shape[2]
        for value_index in range(cards_per_suit):
            # One person is unknown, everybody else doesn't have card
            if np.sum(self.card_distribution[hs, value_index, :]) == 1 - no_of_players:
                owner_index = np.where(self.card_distribution[hs][value_index, :] == 0)[0][0]
                # before changing, check if player status is 1 and if it is 1, change then to 0 then make the deduction
                if self.player_status[hs, owner_index] == 1:
                    self.player_status[hs, owner_index] = 0
                self.card_distribution[hs, value_index, owner_index] = 1
        for player_index in range(no_of_players):
            # Player has an unknown card, only one option for unknown
            if self.player_status[hs, player_index] == 1 and player_index != self.player_index:
                unknown_index_array = np.where(self.card_distribution[hs][:, player_index] == 0)[0]
                if len(unknown_index_array) == 1:
                    # value_index = unknown_index_array[0]
                    self.card_distribution[hs, unknown_index_array[0], :] = -1
                    self.card_distribution[hs, unknown_index_array[0], player_index] = 1
                    self.player_status[hs, player_index] = 0

    """
    Checks if a player can clear some suit (has full knowledge over some suit: always safe to ask)
    """
    def check_for_clear(self):
        added_to_queue = False
        # iterate over all remaining suits
        #print(self.player.get_hand())
        for hs in range(self.num_hs):
            # TODO: check if the player has the suit & full knowledge of the suit
            #if current_player.has_hs(hs) and np.sum(self.card_status[suit_index]) == game.deck.cards_per_suit:
            #print(np.sum(np.max(self.card_distribution[hs], axis=1)))
            if np.max(self.card_distribution[hs, :, self.player_index]) == 1 and \
                    np.sum(np.max(self.card_distribution[hs], axis=1)) == self.num_cards_per_hs:
                # for each card in the suit, add to ask_queue if an opponent is holding the card
                for value in range(self.num_cards_per_hs):
                    owner_index = np.where(self.card_distribution[hs][value, :] == 1)[0]
                    # crash assertion?
                    if len(owner_index) == 0:
                        print(self.player.name, self.card_distribution[hs], "time to crash :(")
                    owner = self.players[owner_index[0]]
                    # on opposing team
                    if owner_index > len(self.players) / 2:
                        card = (hs, value)
                        self.player.ask_queue.append((card, owner))
                        added_to_queue = True
                        #printing
                        print(self.player.name, "knows", owner.name, "has the ", card, "!")
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
