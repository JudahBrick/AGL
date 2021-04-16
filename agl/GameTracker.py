

class GameTracker:

    def __init__(self, opponent_name_or_game: str):
        self.opponent_name_or_game = opponent_name_or_game
        self.games_played = []
        self.wins = 0
        self.losses = 0
        self.win_percentage = 0

    def add_result(self, game_or_player: str, won: bool, score: str):
        if won:
            self.wins += 1
        else:
            self.losses += 1
        self.games_played.append((game_or_player, won, score))

    def __str__(self):
        string: str = self.opponent_name_or_game + ": " \
                      + str(self.wins) + "-" + str(self.losses)
        for game in self.games_played:
            string += game
"""  
make a class that contains
game
 score
 if won
opponnet played
keep those stored in the stats per game sorted via game

do the same but have it sorted via name in this file
and then 

#
"""