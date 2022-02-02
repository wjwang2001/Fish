from deck import Deck
from information import Information
import random
from team import Team
import itertools

class Fish:
    def __init__(self, team1, team2):
        # initialize deck + game constants
        self.num_hs = 9
        self.num_cards_per_hs = 6
        self.can_ask_for_own_card = False
        self.hand_size_public = False
        self.total_turns = 0
        # initialize teams
        self.team1 = team1
        self.team2 = team2
        # initialize players
        self.players = []
        self.players.extend(team1.players)
        self.players.extend(team2.players)
        self.num_players = len(self.players)
        # setup the game
        self.initialize_game_info()
        self.initialize_team_info()
        self.deal_cards()
        self.current_player = self.players[random.randint(0, self.num_players - 1)]

    def initialize_game_info(self):
        for player in self.players:
            player.num_hs = 9
            player.num_cards_per_hs = 6
            player.can_ask_for_own_card = False
            player.hand_size_public = False

    def deal_cards(self):
        # initialize the cards and shuffle them
        cards = list(itertools.product([card for card in range(self.num_hs)], [hs for hs in range(self.num_cards_per_hs)]))
        random.shuffle(cards)

        # determine the number of players and the number of cards each player should receive, then distribute
        cards_per_player = self.num_hs * self.num_cards_per_hs / self.num_players
        for i in range(self.num_players):
            self.players[i].initialize_hand(cards[int(i * cards_per_player): int((i + 1) * cards_per_player)])

    def initialize_team_info(self):
        #TODO: teammates
        for player in self.team1.players:
            player.teammates = []
            player.teammates.extend(self.team1.players)
            player.teammates.remove(player)
            player.opponents = self.team2.players
        for player in self.team2.players:
            player.teammates = []
            player.teammates.extend(self.team2.players)
            player.teammates.remove(player)
            player.opponents = self.team1.players


    def display_all_hands(self):
        for player in self.players:
            print(player.get_hand())

    # updates info +hands for each player
    def update_info(self, current_player, card, next_player, got_card):
        for player in self.players:
            player.update(current_player, card, next_player, got_card)

    def play(self):
        # TODO: implement the win condition (i.e. while no team has won 5+ half suits):
        while self.total_turns < 100:
            card, next_player = self.current_player.get_next()
            # the player is out of cards: switch to a teammate if possible
            if card is None:
                # TODO: update information that someone is out of cards (in all cases in which it can occur)
                # for player in self.players:
                #    if len(player.get_hand) == 0:
                #        for player_to_update in self.players:
                #            player_to_update.update_out_of_cards(player, self)
                # get next card and opponent
                if next_player is None:
                    break
                else:
                    self.current_player = next_player
            # the player can ask for a card:
            else:
                print("Turn", self.total_turns + 1, ":", self.current_player.name, "asks for the", card, "from", next_player.name)
                # TODO: assert that current_player can ask for the card from next_player (opposing team)
                if next_player.has_card(card):
                    print("hit!")
                    self.update_info(self.current_player, card, next_player, got_card=True) # event
                else:
                    print("miss!")
                    self.update_info(self.current_player, card, next_player, got_card=False) # event
                    self.current_player = next_player
                self.total_turns += 1
        # end state debugging
        self.display_all_hands()