import pandas as pd
from leagueDocs import Player


class AGL:
    def __init__(self, player_names: [], schedule: pd.DataFrame, games: [], num_of_weeks: int,
                 games_per_day: int):
        self.players = {}
        for name in player_names:
            self.players[name] = Player.Player(name=name, games=games, num_of_weeks=num_of_weeks, player_names=player_names)
        self.schedule = schedule
        self.num_of_weeks = num_of_weeks
        self.games_per_day = games_per_day
        self.count()
        for player in self.players:
            self.players.get(player).count_win_percentages()

    def count(self):
        week_num = 1
        game_number = 1
        game_per_week = self.games_per_day * 5
        for index, row in self.schedule.iterrows():
            home = row['Home']  # add home wins and losses
            away = row['Away']
            game = row['Game']
            winner = row['Winner']
            loser = row['Loser']
            self.players.get(winner).add_game_result(game=game, opponent=loser, won=True, home=home == winner)
            self.players.get(loser).add_game_result(game=game, opponent=winner, won=False, home=home == loser)
            self.players.get(winner).week_stats.get(week_num).add_game(game=game, win=True)
            self.players.get(loser).week_stats.get(week_num).add_game(game=game, win=False)
            game_number += 1
            if game_number % game_per_week == 0:
                week_num += 1


def win_percentage(wins, losses):
    if wins == losses and losses == 0:
        return 0
    elif losses == 0 and wins != 0:
        return float(100)
    else:
        return round((wins / (wins + losses)) * 100, 1)


gameNames = ['Anagrams', 'Archery', 'Basketball', 'Cup Pong', 'Connect Four', 'Darts', 'Knockout', 'Pool']
playerNames = ['Brick', 'Ennis', 'Hagler', 'Shmuel', 'Zach', 'Judah', 'Siegel', 'Yitzie']
agl = pd.read_csv('copy_of_agl.csv')
agl = agl.dropna()


#print(agl[0:20])
# agl['game_num'] = agl.

# agl['game_number'] = range(1, 1 +len(agl))
# agl.set_index('game_number')
print(agl.head(5))
print(agl.columns)

league = AGL(player_names=playerNames, games=gameNames, schedule=agl, games_per_day=8, num_of_weeks=10)
for player in league.players:
    league.players.get(player).print_per_week_win_ration()

# players = {}
#
#
# for name in playerNames:
#     players[name] = Player.Player(name=name, games=gameNames, player_names=playerNames, num_of_weeks=weeks)
#
#
# for player in players:
#     print()
#     print()
#     players[player].print()
#
# for player in player:
#     players[player].week_stats.get(1)


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

