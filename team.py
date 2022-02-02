class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.points = 0

    def add_player(self, player):
        self.players.append(player)

    def display(self):
        print(self.name, end=': ')
        # assume # of players > 0
        for i in range(len(self.players) - 1):
            print(self.players[i].name, end=', ')
        print(self.players[-1].name, "have", self.points, "points.")

    # future work: declare
    def declare(self, current_player, game, suit_declared):
        print(current_player.name, "declares", suit_declared)
        # declare (need to check for validity first)
        for player in self.players:
            cards_to_remove = []
            for card in player.hand:
                if card.suit == suit_declared:
                    cards_to_remove.append(card)
                    #player.hand.remove(card)
                    card.display()
                    print(" removed from", player.name)
            for card in cards_to_remove:
                player.hand.remove(card)
        for player in game.players:
            player.display_hand()
        # remove cards from deck
        game.deck.suits.remove(suit_declared)
        game.deck.no_of_suits -= 1
        print("suits left", game.deck.suits)
        # add a point to the corresponding team
        current_player.team.points += 1