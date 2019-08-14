from leagueDocs import StatsPerGame, PLayerVsPlayerStats, WeekStats


class Player:

    def __init__(self, name: str, games: [], player_names: [], num_of_weeks: int):
        self.stats = {}
        for game in games:
            self.stats[game] = StatsPerGame.StatsPerGame(game)
        self.name = name
        self.home_wins = 0
        self.home_losses = 0
        self.home_win_percent = 0
        self.away_wins = 0
        self.away_losses = 0
        self.away_win_percent = 0
        self.vs_other_players = PLayerVsPlayerStats.PlayerVsPlayerStats(name, games, player_names)
        self.week_stats = {}
        i = 1
        while i < num_of_weeks + 1:
            self.week_stats[i] = WeekStats.WeekStats(i)
            i += 1

    def get_vs_players(self):
        return self.vs_other_players

    # TODO need to add the effect that this game has to everything
    # that includes:
    # total wins/losses
    # home/away wins/losses
    # general per game wins/losses
    # vs this player total
    # vs this player in this game
    # stats for this week

    def add_game_result(self, game: str, opponent: str, won: bool, home: bool):
        self.stats.get(game).add_result(won=won)
        self.vs_other_players.add_result(opponent=opponent, game=game, won=won)
        self.add_personal_stats(won=won, home=home, game=None, opponent=None)

    def add_personal_stats(self, game: str, opponent: str, won: bool, home: bool):
        if won:
            if home:
                self.home_wins += 1
            else:
                self.away_wins += 1
        else:
            if home:
                self.home_losses += 1
            else:
                self.away_losses += 1

    def count_win_percentages(self):
        self.home_win_percent = win_percentage(self.away_wins, self.home_losses)
        self.away_win_percent = win_percentage(self.away_wins, self.away_losses)
        for stat in self.stats:
            current_game = self.stats.get(stat)
            current_game._win_percentage = win_percentage(current_game.wins, current_game.losses)
        stat_sheet = self.get_vs_players().vs_others
        for stat in stat_sheet:
            current_game = stat_sheet[stat]
            current_game._win_percentage = win_percentage(current_game.wins, current_game.losses)
        stat_sheet = self.get_vs_players().overall_per_player
        for stat in stat_sheet:
            current_game = stat_sheet[stat]
            current_game.win_percentage = win_percentage(current_game.wins, current_game.losses)
    #
    # def init_week_stats(self):
    #     for week in (1, self.num_of_weeks + 1):
    #         self.week_stats[week] = WeekStats(week)

    def print(self):
        print(self.name, " Home ", str(self.home_wins) + ":" + str(self.home_losses),
              " Away ", str(self.away_wins), ":", str(self.away_losses))
        for stat in self.stats:
            print(str(self.stats.get(stat)))
        print(self.get_vs_players())

    def print_week_stats(self):
        print(self.name)
        for week in self.week_stats:
            print(self.week_stats.get(week))

    def print_per_week_win_ration(self):
        print(self.name)
        for week in self.week_stats:
            print(self.week_stats.get(week).just_win_loss_ratio())

def win_percentage(wins, losses):
    if wins == losses and losses == 0:
        return 0
    elif losses == 0 and wins != 0:
        return float(100)
    else:
        return round((wins / (wins + losses)) * 100, 1)