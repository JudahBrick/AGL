from AGL import StatsPerGame, PLayerVsPlayerStats, WeekStats
import pandas as pd


class Player:

    def __init__(self, name: str, games: [], df: pd.DataFrame, player_names: [],
                 games_each_day: int, num_of_weeks: int):
        self.schedule = df
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
        self.vs_other_players = PLayerVsPlayerStats.PLayerVsPlayerStats(name, games, player_names)

        self.games_per_day = games_each_day
        self.num_of_weeks = num_of_weeks
        self.week_stats = {}
        for i in range(1, num_of_weeks):
            self.week_stats[i] = WeekStats.WeekStats(1)


        self.count()
        self.count_win_percentages()

    def get_vs_players(self):
        return self.vs_other_players

    def add_game_result(self, game: str, opponent: str, won: bool, home: bool):
        if won:
            self.stats[game].wins += 1
            self.vs_other_players




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

    def init_week_stats(self):
        for week in (1, self.num_of_weeks + 1):
            self.week_stats[week] = WeekStats(week)

    def print(self):
        print(self.name, " Home ", str(self.home_wins) + ":" + str(self.home_losses),
              " Away ", str(self.away_wins), ":", str(self.away_losses))
        for stat in self.stats:
            print(str(self.stats.get(stat)))
        print(self.get_vs_players())



def win_percentage(wins, losses):
    if wins == losses and losses == 0:
        return 0
    elif losses == 0 and wins != 0:
        return float(100)
    else:
        return round((wins / (wins + losses)) * 100, 1)