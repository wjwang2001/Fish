from deck import Deck
from players import Player
from game import Fish

def sample_probs(a, b, c):
    if a == 0:
        return 0
    if b == 0:
        return 1
    if c == 0:
        return 1
    prob = b * sample_probs(a, b-1, c) + c * (1-sample_probs(b, a, c-1))
    prob = prob/(b+c)
    #print(a, b, c, prob)
    return prob

def test():
    for i in range(1, 6):
        for j in range(1, 6-i + 1):
            c = 6-i-j
            prob = sample_probs(i, j, c)
            print(i, j, c, prob)
    #sample_probs(4, 1, 1)
    print('\u2660', '\u2661', '\u2662', '\u2663')
    print('\u2664', '\u2665', '\u2666', '\u2667')


if __name__ == '__main__':
    test()
    # initialize players
    player1 = Player("Edgar")
    player2 = Player("William")
    player3 = Player("Alina")
    player4 = Player("Lucas")
    player5 = Player("Get Ready")
    player6 = Player("Akanksha")
    players = [player1, player2, player3, player4]

    game = Fish(players)
    #game.play()




