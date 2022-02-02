from players import Player, Computer
from team import Team
from game import Fish

if __name__ == '__main__':
    # initialize players
    player1 = Computer("Edgar")
    player2 = Computer("William")
    player3 = Computer("Alina")
    player4 = Computer("Lucas")
    # initialize teams
    team1 = Team("team1")
    team2 = Team("team2")
    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)
    team2.add_player(player4)
    # debug display
    team1.display()
    team2.display()
    # start game
    game = Fish(team1, team2)
    game.play()




