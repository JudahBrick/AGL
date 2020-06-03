from leagueDocs.agl import PLayerVsPlayerStats, StatsPerGame, WeekStats


class Player:

    def __init__(self, name: str, games: [], player_names: [], num_of_weeks: int, east_division: bool):
        self.stats = {}
        self.games = []
        self.list_of_win_percentage = []
        self.list_of_wins = []
        self.list_of_losses = []
        self.stack_of_wins = []
        self.dict_of_win_percent = {}
        self.rank = {}
        self.total_wins = 0
        self.total_losses = 0
        for game in games:
            self.stats[game] = StatsPerGame.StatsPerGame(game)
        self.name = name
        self.east_division = east_division
        self.division_wins = 0
        self.division_losses = 0
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

    def get_stats(self):
        return self.stats

    # TODO need to add the effect that this game has to everything
    # that includes:
    # total wins/losses
    # home/away wins/losses
    # general per game wins/losses
    # vs this player total
    # vs this player in this game
    # stats for this week

    def add_game_result(self, game: str, opponent: str, won: bool, home: bool, opp_in_eastern_division: bool,
                        score: str):
        # print(self.name + " " + game + " " + opponent)
        self.games.append(game + "&" + opponent + "&" + str(won) + "&" + score)  # for schedule difficulty look up
        self.stats.get(game).add_result(won=won, score=score)
        self.vs_other_players.add_result(opponent=opponent, game=game, won=won, score=score)
        self.add_personal_stats(won=won, home=home, opp_in_eastern_division=opp_in_eastern_division, game=None,
                                opponent=None)
        self.list_of_win_percentage.append(win_percentage(self.total_wins, self.total_losses))
        self.dict_of_win_percent[self.total_losses + self.total_wins] \
            = win_percentage(self.total_wins, self.total_losses)
        self.list_of_wins.append(self.total_wins)
        self.list_of_losses.append(self.total_losses)

    def add_personal_stats(self, game: str, opponent: str,
                           won: bool, home: bool, opp_in_eastern_division: bool) -> None:
        if won:
            self.stack_of_wins.append(True)
            self.total_wins += 1
            if home:
                self.home_wins += 1
            else:
                self.away_wins += 1
            if self.east_division == opp_in_eastern_division:
                self.division_wins += 1
        else:
            self.total_losses += 1
            self.stack_of_wins.append(False)
            if home:
                self.home_losses += 1
            else:
                self.away_losses += 1
            if self.east_division == opp_in_eastern_division:
                self.division_losses += 1

    def count_win_percentages(self) -> None:
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
        for week in self.week_stats:
            current_week = self.week_stats.get(week)
            current_week.win_percentage = win_percentage(current_week.wins, current_week.losses)

    # this is supposed to count a player's record over the past n games
    # we don't really use this cas theres a bug and its not that crucial
    def count_record_for_last_n(self, n: int) -> str:
        stack = self.stack_of_wins.copy()
        wins = 0
        losses = 0
        i = 0
        while i < n and i < len(stack):
            if stack.pop():
                wins += 1
            else:
                losses += 1
            i += 1
        return str(wins) + "-" + str(losses)

    #
    # def init_week_stats(self):
    #     for week in (1, self.num_of_weeks + 1):
    #         self.week_stats[week] = WeekStats(week)

    def print(self) -> None:
        print(self.name, " Home ", str(self.home_wins) + ":" + str(self.home_losses),
              " Away ", str(self.away_wins), ":", str(self.away_losses))
        for stat in self.stats:
            print(str(self.stats.get(stat)))
        self.print_week_stats()
        print(self.get_vs_players())

    def print_week_stats(self) -> None:
        print(self.name)
        for week in self.week_stats:
            print(self.week_stats.get(week))

    def print_per_week_win_ration(self) -> None:
        print(self.name)
        for week in self.week_stats:
            print(self.week_stats.get(week).just_win_loss_ratio())

    def print_division_record(self) -> None:
        out_of_division_wins = self.total_wins - self.division_wins
        out_of_division_losses = self.total_losses - self.division_losses
        print("Record: " + str(self.total_wins) + ":" + str(self.total_losses))
        print("Division Record: " + str(self.division_wins) + ":" + str(self.division_losses))
        print("Out Of Division Record: " + str(out_of_division_wins) + ":" + str(out_of_division_losses))



def win_percentage(wins: int, losses: int) -> float:
    if wins == losses and losses == 0:
        return 0
    elif losses == 0 and wins != 0:
        return float(100)
    else:
        return round((wins / (wins + losses)) * 100, 1)
