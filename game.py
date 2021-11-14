from deck import Deck
from information import Information
import random
from team import Team


class Fish:
    def __init__(self, players, teams=2):
        self.deck = Deck()
        self.players = players
        for i in range(len(players)):
            players[i].index = i
        # teams (first draft of code)
        assert len(self.players) % teams == 0
        self.teams = [Team(i) for i in range(teams)]
        for i in range(len(self.teams)):
            team = self.teams[i]
            team.add_players(players[i * teams: (i+1) * teams])
            team.display()
        # setup the game
        self.deck.shuffle()
        self.deck.deal(self.players)
        self.current_player = self.players[random.randint(0, len(self.players) - 1)]
        # players know the composition of the deck (has to be after dealing)
        for player in self.players:
            player.deck = self.deck
            player.information = Information(player.deck, players, player)
        # information not public to human players
        #self.information = Information(self.deck, self.players) #teams too probably
        self.total_turns = 0

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
                for player_out_of_card in self.players:
                    # make sure to only do this for computerized players
                    if len(player_out_of_card.hand) == 0 and player.name != player_out_of_card.name:
                        player.information.update_out_of_cards(player_out_of_card, self)
            # get next card and opponent
            card, next_player = self.current_player.get_next(self)
            # the player is out of cards: switch to a teammate if possible
            if card is None:
                # TODO: update information that someone is out of cards (in all cases in which it can occur)
                for player in self.players:
                    # make sure to only do this for computerized players
                    if player.name != self.current_player.name:
                        player.information.update_out_of_cards(self.current_player, self)
                if next_player is None:
                    break
                else:
                    self.current_player = next_player
            # the player can ask for a card:
            else:
                print("Turn", self.total_turns + 1, ":", self.current_player.name, "asks for the ", end='')
                card.display()
                print(" from", next_player.name, end='. ')
                # TODO: assert that current_player can ask for the card from next_player (opposing team)
                if next_player.has_card(card):
                    print("hit!")
                    #self.information.update(self.current_player, card, next_player, got_card=True)
                    self.update_info(self.current_player, card, next_player, got_card=True)
                    next_player.hand.remove(card)
                    self.current_player.hand.append(card)
                    self.display_all_hands()
                else:
                    print("miss!")
                    #self.information.update(self.current_player, card, next_player, got_card=False)
                    self.update_info(self.current_player, card, next_player, got_card=False)
                    self.current_player = next_player
                self.total_turns += 1

        # TODO: let opposing team try to declare
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

        #print(self.information.info_public)
        #for player in self.players:
        #    print(player.name, player.information.info_public)
        self.display_all_hands()
        for team in self.teams:
            team.display()
