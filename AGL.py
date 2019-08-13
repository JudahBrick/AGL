import numpy as np
import pandas as pd


class AGL:
    def __init__(self, player_names: [], schedule: pd.DataFrame, games: [], num_of_weeks: int,
                 games_per_day_per_player: int):
        self.players = {}


def count(self):
     # for game_stat in self._stats:
     print(self.name)
     # df = self._schedule.loc[self._schedule['Winner'] == self._name]
         # game_stat._game
     num_of_week = 1
     game_number = 0
     game_per_week = 10 #self._games_per_day * 5
     for index, row in self.schedule.iterrows():
         print(index)
         home = row['Home']  #add home wins and losses
         away = row['Away']
         game = row['Game']
         loser = row['Loser']
         self.stats.get(game).wins += 1
         self.get_vs_players().vs_others[loser + "_" + game].wins += 1
         self.get_vs_players().overall_per_player[loser].wins += 1
         self.week_stats.get(num_of_week).add_game(game, True)
         if home == self.name:
             self.home_wins += 1
         elif away == self.name:
             self.away_wins += 1
         if game_number % game_per_week == 0:
             num_of_week += 1
        #
        num_of_week = 1
        game_number = 0
        df = self.schedule.loc[self.schedule['Loser'] == self.name]
        for index, row in df.iterrows():
            game_number += 1
            home = row['Home']
            away = row['Away']
            game = row['Game']
            winner = row['Winner']
            self.stats.get(game).losses += 1
            self.get_vs_players().overall_per_player[winner].losses += 1
            self.get_vs_players().vs_others[winner + "_" + game].losses += 1
            self.week_stats.get(num_of_week).add_game(game, False)

            if home == self.name:
                self.home_losses += 1
            elif away == self.name:
                self.away_losses += 1
            if game_number % game_per_week == 0:
                num_of_week += 1


def win_percentage(wins, losses):
    if wins == losses and losses == 0:
        return 0
    elif losses == 0 and wins != 0:
        return float(100)
    else:
        return round((wins / (wins + losses)) * 100, 1)

games = ['Anagrams', 'Archery', 'Basketball', 'Cup Pong',
         'Connect Four', 'Darts', 'Knockout', 'Pool']
player_names = ['Brick', 'Ennis', 'Hagler', 'Shmuel', 'Zach', 'Judah', 'Siegel', 'Yitzie']
agl = pd.read_csv('copy_of_agl.csv')
agl = agl.dropna()
number_of_games_per_day = 2
weeks = 10

#print(agl[0:20])
# agl['game_num'] = agl.

# agl['game_number'] = range(1, 1 +len(agl))
# agl.set_index('game_number')
print(agl.head(5))
print(agl.columns)

players = {}

for name in player_names:
    players[name] = Player(name=name, df=agl, games=games, player_names=player_names,
                           games_each_day=number_of_games_per_day, num_of_weeks=weeks)


for player in players:
    print()
    print()
    players[player]._print()

for player in player:
    players[player].week_stats.get(1)


print()
print()
print()
print()
print("######    iterating  ######")
# row = next(agl.iteritems())
agl = agl.tail(10)


for index, row in agl.iterrows():
    home = row['Home']
    away = row['Away']
    game = row ['Game']
    winner = row['Winner']
    loser = row['Loser']
    print(winner + " beat " + loser + " in " + game)

agl = agl.tail(10)

