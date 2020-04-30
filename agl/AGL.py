import pandas as pd
from leagueDocs.agl import Player
from leagueDocs.agl.analysis.DataCollector import DataCollector


# this calss holds all of the per season needed data.

class AGL:
    # this collects all of the data on each game, across all of the season.
    # we hope to use the data to gage average scores and how impressive a win is
    data_collector: DataCollector = DataCollector(
        ['Basketball', 'Cup Pong', 'Darts', 'Knockout', 'Pool', "Shuffleboard", "Golf"])

    def __init__(self, player_names: [], schedule: pd.DataFrame, games: [], num_of_weeks: int,
                 games_per_day: int, east: []):
        self.players = {}
        for name in player_names:
            self.players[name] = Player.Player(name=name, games=games, num_of_weeks=num_of_weeks,
                                               player_names=player_names, east_division=name in east)

        self.schedule = schedule
        self.num_of_weeks = num_of_weeks
        self.games_per_day = games_per_day
        self.count()
        for player in self.players:
            self.players.get(player).count_win_percentages()

    # This will run through the  dataframe (the schedule tab on the doc)
    # and will input each game and convert it into the python POPOs (PLain Old Python Objects)
    def count(self):
        # game_number = 0
        # week_num = 1
        # game_per_week = self.games_per_day * 5
        for index, row in self.schedule.iterrows():
            home_player = row['Home']  # add home wins and losses
            away = row['Away']
            game = row['Game']
            winner = row['Winner']
            loser = row['Loser']
            score = row['Score']
            week_num = row['Week']

            if game == "Word Hunt":
                game = "Word_Hunt"
            if winner == loser:
                print("##########   loser == winner?!  ########")
                print(game + " " + winner + " " + loser + "     Score: " + score)
            self.players.get(winner).add_game_result(game=game, opponent=loser, won=True, home=home_player == winner,
                                                     opp_in_eastern_division=self.players.get(loser).east_division,
                                                     score=score)
            self.players.get(loser).add_game_result(game=game, opponent=winner, won=False, home=home_player == loser,
                                                    opp_in_eastern_division=self.players.get(winner).east_division,
                                                    score=score)
            # print('Week Num: ' + week_num)
            self.players.get(winner).week_stats.get(int(week_num)).add_game(game=game, win=True)
            self.players.get(loser).week_stats.get(int(week_num)).add_game(game=game, win=False)
            # print('Game Number: ' + str(game_number) + '  Week Number: ' + str(week_num))
            # game_number += 1
            # if game_number % game_per_week == 0:
            #     week_num += 1
