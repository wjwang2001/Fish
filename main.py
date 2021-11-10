from deck import Deck
from players import Player
from game import Fish

if __name__ == '__main__':
    # initialize players
    player1 = Player("Edgar")
    player2 = Player("William")
    player3 = Player("Alina")
    player4 = Player("Lucas")
    player5 = Player("Get Ready")
    player6 = Player("Akanksha")
    players = [player1, player2, player3, player4]

    game = Fish(players)
    game.play()




