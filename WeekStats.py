
class WeekStats:
    def __init__(self, week: int):
        self.week = week
        self.wins = 0
        self.losses = 0
        self.won_games = []
        self.lost_games = []
        self.win_percentage = 0

    def add_game(self, game: str, win: bool):
        if win:
            self.wins += 1
            self.won_games.append(game)
        else:
            self.losses += 1
            self.lost_games.append(game)

    def just_win_loss_ratio(self):
        return str(self.wins) + "-" + str(self.losses) + ": " + str(int(self.win_percentage)) + "%"

    def __str__(self):
        rtn = "Week #" + str(self.week) + ": " + str(self.wins) + "-" + str(self.losses) \
               + "\n" + "  Won Games:"
        for game_played in self.won_games:
            rtn += " "
            rtn += game_played
        rtn += "\n  Lost Game:"
        for game_played in self.lost_games:
            rtn += " "
            rtn += game_played

        return rtn
