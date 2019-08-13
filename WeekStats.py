

class WeekStats:
    def __init__(self, week: int):
        self.week = week
        self.wins = 0
        self.losses = 0
        self.won_games = []
        self.lost_games = []


    def add_game(self, game: str, win: bool):
        if win:
            self.wins += 1
            self.won_games.append(game)
        else:
            self.losses += 1
            self.lost_games.append(game)

    def __str__(self):
        rtn = "Week #" + str(self.week) + ": " + str(self.wins) + "-" + str(self.losses) \
               + "\n" + "Lost Games: "
        for game_played in self.won_games:
            rtn += " "
            rtn += game_played
        for game_played in self.lost_games:
            rtn += " "
            rtn += game_played
