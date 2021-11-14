from deck import Deck
from information import Information
import random
from team import Team
import itertools

class Fish:
    def __init__(self, players, num_hs=6, num_cards_per_hs=9):
        # initialize players
        self.players = players
        # make teams
        self.assign_teams()
        # deal cards
        self.num_hs = num_hs
        self.num_cards_per_hs = num_cards_per_hs
        self.deal_cards()

        # setup the game
        self.total_turns = 0
        self.current_player = self.players[random.randint(0, len(self.players) - 1)]

    def deal_cards(self):
        # initialize the cards and shuffle them
        cards = list(itertools.product([card for card in range(self.num_cards_per_hs)], [hs for hs in range(self.num_hs)]))
        random.shuffle(cards)

        # determine the number of players and the number of cards each player should receive, then distribute
        num_players = len(self.players)
        cards_per_player = self.num_hs * self.num_cards_per_hs / num_players
        for i in range(num_players):
            self.players[i].initialize_information(cards[int(i * cards_per_player): int((i + 1) * cards_per_player)])

    def assign_teams(self, teams=2):
        num_of_players = len(self.players)
        assert num_of_players % teams == 0
        team1 = self.players[:num_of_players // 2]
        team2 = self.players[num_of_players // 2:]
        for player in self.players:
            player.initialize_p2i(team1, team2)

    def display_all_hands(self):
        for player in self.players:
            player.display_hand()
        print()

    # updates info for each player
    def update_info(self, current_player, card, next_player, got_card):
        for player in self.players:
            # make sure to only do this for computerized players
            player.information.update(current_player, card, next_player, got_card)

    def play(self):
        self.display_all_hands()
        # TODO: implement the win condition (i.e. while no team has won 5+ half suits):
        while self.total_turns < 1000:
            # TODO: update information that someone is out of cards (in all cases in which it can occur)
            for player in self.players:
                if len(player.get_hand) == 0:
                    for player_to_update in self.players:
                        player_to_update.update_out_of_cards(player, self)
            # get next card and opponent
            card, next_player = self.current_player.get_next(self)
            # the player is out of cards: switch to a teammate if possible
            if card is None:
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
                    self.update_info(self.current_player, card, next_player, got_card=True)
                else:
                    print("miss!")
                    self.update_info(self.current_player, card, next_player, got_card=False)
                    self.current_player = next_player
                self.total_turns += 1

        # TODO: let opposing team try to declare
        """
        for player in self.players:
            for player_out_of_card in self.players:
                # make sure to only do this for computerized players
                if len(player_out_of_card.hand) == 0 and player.name != player_out_of_card.name:
                    player.information.update_out_of_cards(player_out_of_card, self)
        # get the other team random player
        random_opponent = self.players[random.randint(0, len(self.players)-1)]
        while self.current_player.team == random_opponent.team:
            random_opponent = self.players[random.randint(0, len(self.players)-1)]
        print(self.current_player.name, "team ran out of cards, switch to", random_opponent.name)
        card, next_player = random_opponent.get_next(self)
        """
        self.display_all_hands()
