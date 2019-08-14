

class StatsPerGame:
    def __init__(self, game: str):
        self.game = game
        self.wins = 0
        self.losses = 0
        self.win_percentage = 0

    def add_result(self, won: bool):
        if won :
            self.wins += 1
        else:
            self.losses += 1

    def __str__(self):
        return self.game + " " + str(self.wins) + ":" + str(self.losses) \
               + "   " + str(self.win_percentage) + "%"
#          + " " + str(self._wins/self._losses) + "%"
