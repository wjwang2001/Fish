from card import Card
from random import shuffle


class Deck:
    def __init__(self, num_of_decks=1):
        self.cards = []
        Suits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        Values = ['\u2654', '\u2655', '\u2656', '\u2657', '\u2658', '\u2659']
        standard_deck = []
        for i in range(len(Suits)):
            for j in range(len(Values)):
                card = Card(Suits[i], Values[j])
                card.suit_index = i
                card.value_index = j
                standard_deck.append(card)
        for deck in range(num_of_decks):
            self.cards.extend(standard_deck)
        # fish specific
        self.suits = Suits
        self.no_of_suits = len(self.suits)
        self.values = Values
        self.cards_per_suit = len(self.values)




    def shuffle(self):
        shuffle(self.cards)

    def deal(self, players):
        num_cards = len(self.cards) / len(players)
        for player_index in range(len(players)):
            lower_index = int(player_index * num_cards)
            upper_index = int((player_index + 1) * num_cards)
            players[player_index].hand = self.cards[lower_index: upper_index]